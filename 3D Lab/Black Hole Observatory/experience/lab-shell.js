/* Shared lifecycle for the independently published scene entries. */
const labScene = (() => {
  let entered = false
  let ready = false
  let displayed = false
  let retryTimer

  function revealScene() {
    if (!entered || !ready || !displayed) return
    requestAnimationFrame(() => requestAnimationFrame(() => {
      document.getElementById('lab-construction').hidden = true
      clearTimeout(retryTimer)
    }))
  }

  function begin() {
    entered = true
    const screen = document.getElementById('lab-construction')
    screen.hidden = false
    displayed = false
    // Show one assembly cycle on entry, then dismiss as soon as the renderer is ready.
    const animation = getComputedStyle(screen.querySelector('.lab-bench'))
    const duration = parseFloat(animation.animationDuration) * 1000 || 0
    setTimeout(() => { displayed = true; revealScene() }, duration)
    clearTimeout(retryTimer)
    retryTimer = setTimeout(() => { screen.querySelector('button').hidden = false }, 20000)
    revealScene()
  }

  function markReady() {
    ready = true
    revealScene()
  }

  async function prepareIntroduction(video, buttons) {
    const source = new URL(video.dataset.src, location.href)
    const key = new URL('/__lab-media/' + video.dataset.sha256, location.origin)
    const expectedSize = Number(video.dataset.bytes)
    const cache = await window.caches?.open('open-science-introductions-v1').catch(() => undefined)
    const saved = await cache?.match(key).catch(() => undefined)
    let recording = await saved?.blob().catch(() => undefined)
    if (recording?.size !== expectedSize) {
      const response = await fetch(source, { credentials: 'omit' })
      if (response.status !== 200) throw new Error('Introduction download failed')
      recording = await response.blob()
      if (recording.size !== expectedSize) throw new Error('Incomplete introduction')
      if (window.crypto?.subtle) {
        const digest = await crypto.subtle.digest('SHA-256', await recording.arrayBuffer())
        const checksum = Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('')
        if (checksum !== video.dataset.sha256) throw new Error('Introduction checksum mismatch')
      }
      await cache?.put(key, new Response(recording)).catch(() => undefined)
    }
    video.src = URL.createObjectURL(recording)
    for (const button of buttons) {
      button.disabled = false
      button.dataset.labWatch = 'ready'
      button.textContent = 'Watch introduction'
    }
  }

  function loadIntroduction() {
    const video = document.querySelector('video[data-src]')
    const buttons = [...document.querySelectorAll('[data-lab-watch]')]
    const load = () => {
      for (const button of buttons) {
        button.textContent = 'Loading resources'
        button.disabled = true
      }
      prepareIntroduction(video, buttons).catch(() => {
        for (const button of buttons) {
          button.textContent = 'Retry loading introduction'
          button.disabled = false
          button.addEventListener('click', retry, { capture: true })
        }
      })
    }
    function retry(event) {
      event.stopImmediatePropagation()
      for (const button of buttons) button.removeEventListener('click', retry, true)
      load()
    }
    load()
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#lab-construction button').onclick = () => location.reload()
    loadIntroduction()

    const actions = document.querySelector('[data-lab-import]').parentElement
    const panel = document.querySelector('[data-lab-inside]')
    actions.setAttribute('data-lab-actions', '')
    function alignPanel() {
      if (!panel.getClientRects().length) return
      const bounds = actions.getBoundingClientRect()
      if (!bounds.width) return
      const parent = panel.offsetParent
      const origin = parent ? parent.getBoundingClientRect().left + parent.clientLeft : 0
      panel.style.left = (bounds.left - origin) + 'px'
      panel.style.width = bounds.width + 'px'
      panel.style.right = 'auto'
      panel.style.boxSizing = 'border-box'
    }
    const resize = new ResizeObserver(alignPanel)
    resize.observe(actions)
    resize.observe(panel)
    window.addEventListener('resize', alignPanel)
    alignPanel()
  })

  return { begin, markReady }
})()
