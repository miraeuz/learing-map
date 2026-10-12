/** Small UI event channels: toast messages and confetti bursts. */
export const toast = $state({ id: 0, text: '', tone: 'gold' as 'gold' | 'teal' | 'ink' });

export function showToast(text: string, tone: 'gold' | 'teal' | 'ink' = 'gold') {
  toast.text = text;
  toast.tone = tone;
  toast.id++;
}

export const confetti = $state({ id: 0, x: 0, y: 0 });

export function burst(x: number, y: number) {
  confetti.x = x;
  confetti.y = y;
  confetti.id++;
}
