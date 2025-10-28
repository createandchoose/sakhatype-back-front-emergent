// Sound manager
export class SoundManager {
  private sounds: Map<string, HTMLAudioElement> = new Map()
  private enabled: boolean = true

  constructor() {
    this.enabled = localStorage.getItem('soundEnabled') !== 'false'
  }

  loadSound(name: string, url: string) {
    const audio = new Audio(url)
    this.sounds.set(name, audio)
  }

  play(name: string) {
    if (!this.enabled) return
    
    const sound = this.sounds.get(name)
    if (sound) {
      sound.currentTime = 0
      sound.play().catch(e => console.error('Failed to play sound:', e))
    }
  }

  setEnabled(enabled: boolean) {
    this.enabled = enabled
    localStorage.setItem('soundEnabled', String(enabled))
  }

  isEnabled(): boolean {
    return this.enabled
  }
}

export const soundManager = new SoundManager()

// Placeholder sound URLs - user will add actual sound files
export const SOUND_URLS = {
  keypress: '/sounds/keypress.mp3',
  error: '/sounds/error.mp3',
  complete: '/sounds/complete.mp3',
  click: '/sounds/click.mp3',
}

// Initialize sounds
Object.entries(SOUND_URLS).forEach(([name, url]) => {
  soundManager.loadSound(name, url)
})
