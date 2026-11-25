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

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#lab-construction button').onclick = () => location.reload()
    const video = document.querySelector('video')
    const status = document.getElementById('lab-media-status')
    const setMediaStatus = () => {
      const waiting = !video.error && !video.ended &&
        (video.readyState < 1 || (!video.paused && video.readyState < 3))
      status.hidden = !waiting
    }
    for (const name of ['loadstart','loadedmetadata','play','waiting','canplay','playing','pause','ended','error']) {
      video.addEventListener(name, setMediaStatus)
    }
    setMediaStatus()

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
