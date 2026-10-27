"""Optional video references: schema, remote probes and local metadata."""
import argparse
from contextlib import closing
import hashlib
from html.parser import HTMLParser
from http.client import HTTPException, HTTPSConnection
import ipaddress
import json
from pathlib import Path
import re
import socket
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, unquote, urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, HTTPSHandler, ProxyHandler, Request, build_opener


S3_BUCKET = 'statics-aipochcom-prod'
S3_PREFIX = 'open-science/usecases/'
VIDEO_EXTENSIONS = ('.mp4', '.webm', '.mov', '.m4v', '.avi', '.mkv', '.ogv', '.mpeg', '.mpg')
OEMBED_URL = 'https://www.youtube.com/oembed'


def https_url(value):
    if not isinstance(value, str) or re.search(r'[\s\x00-\x1f\x7f\\]', value):
        return False
    try:
        url = urlsplit(value)
        return (url.scheme == 'https' and bool(url.hostname) and not url.username
                and not url.password and url.port in (None, 443) and not url.fragment)
    except ValueError:
        return False


def youtube_id(value):
    if not https_url(value):
        return None
    url = urlsplit(value)
    host = url.hostname.lower()
    parts = url.path.strip('/').split('/')
    if host == 'youtu.be' and len(parts) == 1:
        candidate = parts[0]
    elif host in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
        if url.path == '/watch':
            values = parse_qs(url.query).get('v', [])
            candidate = values[0] if len(values) == 1 else ''
        elif len(parts) == 2 and parts[0] in ('shorts', 'embed', 'live'):
            candidate = parts[1]
        else:
            return None
    else:
        return None
    return candidate if re.fullmatch(r'[A-Za-z0-9_-]{11}', candidate) else None


def video_errors(entry):
    if 'video' not in entry:
        return []
    from check_structure import require_keys, validate_resource_path
    video, errors = entry['video'], []
    label = str(entry.get('name')) + '/video'
    if not isinstance(video, dict):
        return [label + ': expected an object']
    kind = video.get('type')
    if kind not in ('s3', 'external', 'youtube'):
        return [label + ': type must be s3, external or youtube']
    required = {'type', 'file_path', 'file_name'}
    if kind != 'youtube':
        required.add('bytes')
    if kind == 's3':
        required.add('sha256')
    if not require_keys(video, required, label, errors, optional=('bytes', 'sha256')):
        return errors
    path, filename = video['file_path'], video['file_name']
    if (not isinstance(filename, str) or not filename.strip()
            or re.search(r'[\x00-\x1f\x7f/\\]', filename)):
        errors.append(label + ': file_name must be a nonempty filename or YouTube display name')
    elif kind != 'youtube' and not filename.lower().endswith(VIDEO_EXTENSIONS):
        errors.append(label + ': unsupported video file extension')
    if kind != 'youtube' and (type(video['bytes']) is not int or video['bytes'] <= 0):
        errors.append(label + ': bytes must be a positive integer')
    if kind == 's3':
        try:
            validate_resource_path({'path': path, 'file_name': filename})
            if path != str(entry.get('name')) + '/' + filename or '%' in path:
                raise ValueError('file_path must be {case.name}/{file_name}, without encoded segments')
            if any(isinstance(entry.get(k), dict) and filename == entry[k].get('file_name')
                   for k in ('cover', 'case', 'introduction')):
                raise ValueError('video destination collides with another resource')
        except ValueError as error:
            errors.append(label + ': ' + str(error))
        if not isinstance(video['sha256'], str) or not re.fullmatch(r'[0-9a-fA-F]{64}', video['sha256']):
            errors.append(label + ': sha256 must be 64 hexadecimal digits')
    elif not https_url(path):
        errors.append(label + ': file_path must be a complete HTTPS URL without credentials or fragments')
    elif kind == 'youtube' and not youtube_id(path):
        errors.append(label + ': expected a supported YouTube single-video URL')
    else:
        decoded = urlsplit(path).path
        while True:
            if (re.search(r'[\x00-\x1f\x7f\\]', decoded)
                    or any(part in ('.', '..') for part in decoded.split('/'))):
                errors.append(label + ': URL path traversal is forbidden')
                break
            following = unquote(decoded)
            if following == decoded:
                break
            decoded = following
    return errors


def check_public_url(url):
    if not https_url(url):
        raise ValueError('video request requires a public HTTPS URL without credentials')
    host = urlsplit(url).hostname
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
        raise ValueError('video request cannot target a private or special-use address')
    return addresses


def connect_addresses(addresses, timeout, source_address=None):
    last_error = None
    for family, kind, protocol, _, address in addresses:
        connection = socket.socket(family, kind, protocol)
        try:
            connection.settimeout(timeout)
            if source_address:
                connection.bind(source_address)
            connection.connect(address)
            return connection
        except BaseException as error:
            connection.close()
            if not isinstance(error, OSError):
                raise
            last_error = error
    raise last_error or OSError('No validated video address')


class PublicHTTPSHandler(HTTPSHandler):
    def https_open(self, req):
        addresses = req.video_addresses

        def connection(host, **kwargs):
            result = HTTPSConnection(host, **kwargs)
            # Pin validated DNS results; HTTPSConnection retains the hostname for TLS/SNI.
            result._create_connection = lambda address, timeout, source_address=None: connect_addresses(
                addresses, timeout, source_address)
            return result

        return self.do_open(connection, req, context=self._context)


class VideoRedirect(HTTPRedirectHandler):
    max_redirections = 5
    max_repeats = 2

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        addresses = check_public_url(newurl)
        redirected = super().redirect_request(req, fp, 307 if code == 308 else code, msg, headers, newurl)
        if redirected is not None:
            redirected.method = req.get_method()
            redirected.video_addresses = addresses
        return redirected

    http_error_308 = HTTPRedirectHandler.http_error_302


def request(url, method):
    # Video requests never forward AWS credentials or use environment HTTP proxies.
    for attempt in range(3):
        try:
            addresses = check_public_url(url)
            req = Request(url, method=method, headers={'Accept-Encoding': 'identity'})
            req.video_addresses = addresses
            return build_opener(ProxyHandler({}), PublicHTTPSHandler(), VideoRedirect()).open(req, timeout=15)
        except HTTPError as error:
            code = error.code
            error.close()
            if code not in (429, 500, 502, 503, 504):
                raise ValueError('video resource is unavailable (HTTP {})'.format(code)) from None
        except (URLError, OSError, HTTPException):
            pass
        if attempt < 2:
            time.sleep(attempt + 1)
    raise ValueError('video probe could not complete after three attempts; retry later')


def check_external(url, size):
    with request(url, 'HEAD') as response:
        if response.status != 200:
            raise ValueError('video HEAD must return HTTP 200')
        length = response.headers.get('Content-Length', '')
        if not re.fullmatch(r'[0-9]+', length) or int(length) != size:
            raise ValueError('video HEAD Content-Length does not match bytes')
        if not response.headers.get_content_type().lower().startswith('video/'):
            raise ValueError('video HEAD must return a video/* Content-Type')


class EmbedParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == 'iframe':
            self.sources.append(dict(attrs).get('src', ''))


def check_youtube(url):
    video_id = youtube_id(url)
    if not video_id:
        raise ValueError('invalid YouTube single-video URL')
    endpoint = OEMBED_URL + '?' + urlencode({'url': 'https://www.youtube.com/watch?v=' + video_id,
                                           'format': 'json'})
    with request(endpoint, 'GET') as response:
        if response.status != 200:
            raise ValueError('YouTube probe must return HTTP 200')
        body = response.read(65537)
        if len(body) > 65536:
            raise ValueError('YouTube metadata exceeds 64 KiB')
    try:
        data = json.loads(body)
    except (ValueError, UnicodeError):
        raise ValueError('YouTube did not return valid video metadata') from None
    if (not isinstance(data, dict) or data.get('type') != 'video'
            or data.get('provider_name') != 'YouTube' or not isinstance(data.get('title'), str)
            or not data['title'].strip() or not isinstance(data.get('html'), str)):
        raise ValueError('YouTube did not confirm a video resource')
    parser = EmbedParser()
    parser.feed(data['html'])
    if not any(youtube_id(src) == video_id for src in parser.sources):
        raise ValueError('YouTube metadata does not identify the requested video')


def s3_head(path):
    import boto3.session
    from botocore.config import Config
    from botocore.exceptions import BotoCoreError, ClientError
    try:
        with closing(boto3.session.Session().client('s3', config=Config(
                connect_timeout=15, read_timeout=15,
                retries={'mode': 'standard', 'total_max_attempts': 3}))) as client:
            return client.head_object(Bucket=S3_BUCKET, Key=S3_PREFIX + path)
    except (BotoCoreError, ClientError):
        raise ValueError('S3 video HEAD failed; check credentials, region, access and object existence') from None


def validate_video(entry):
    errors = video_errors(entry)
    if errors:
        raise ValueError('; '.join(errors))
    video = entry.get('video')
    if video is None:
        return
    if video['type'] == 's3':
        head = s3_head(video['file_path'])
        checksum = head.get('Metadata', {}).get('sha256') if isinstance(head, dict) else None
        if (not isinstance(head, dict) or type(head.get('ContentLength')) is not int
                or head['ContentLength'] != video['bytes'] or not isinstance(checksum, str)
                or checksum.lower() != video['sha256'].lower()):
            raise ValueError('S3 video size or Metadata.sha256 does not match the manifest')
    elif video['type'] == 'external':
        check_external(video['file_path'], video['bytes'])
    else:
        check_youtube(video['file_path'])


def changed_videos(step):
    before, after = step.get('before'), step.get('after')
    old = {e['name']: e for e in (before if isinstance(before, list) else [before]) if isinstance(e, dict)}
    return [e for e in (after if isinstance(after, list) else [after]) if isinstance(e, dict)
            and e.get('video') is not None and e.get('video') != old.get(e['name'], {}).get('video')]


def metadata(path, name):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('case must be the existing manifest kebab-case name')
    if not path.is_file() or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('video must be a regular local file without symlink parents')
    checksum, size = hashlib.sha256(), 0
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            size += len(chunk)
            checksum.update(chunk)
    return {'type': 's3', 'file_path': name + '/' + path.name, 'file_name': path.name,
            'bytes': size, 'sha256': checksum.hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    local = commands.add_parser('metadata', help='Print measured S3 video JSON; never upload or edit manifest')
    local.add_argument('--case', required=True)
    local.add_argument('file', type=Path)
    args = parser.parse_args()
    video = metadata(args.file.absolute(), args.case)
    errors = video_errors({'name': args.case, 'video': video})
    if errors:
        raise ValueError('; '.join(errors))
    print(json.dumps(video, indent=2, ensure_ascii=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as error:
        print('Video metadata failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
