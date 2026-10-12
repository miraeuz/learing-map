/** Typed access to the Electron activation bridge (window.icpc). */

export interface LicenseStatus {
  configured: boolean;
  activated: boolean;
  name: string;
  activatedAt: number;
  pending: boolean;
  expiresAt: number;
  resendAt: number;
}

export type LicenseError =
  | 'name' | 'not_configured' | 'cooldown' | 'network' | 'telegram'
  | 'no_code' | 'expired' | 'format' | 'wrong' | 'too_many';

export interface RequestResult { ok: boolean; error?: LicenseError; expiresAt?: number; resendAt?: number; retryAt?: number; detail?: string }
export interface VerifyResult { ok: boolean; error?: LicenseError; left?: number; name?: string }

interface Bridge {
  license: {
    status(): Promise<LicenseStatus>;
    request(name: string): Promise<RequestResult>;
    verify(code: string): Promise<VerifyResult>;
    rename(name: string): Promise<{ ok: boolean }>;
  };
}

declare global {
  interface Window { icpc?: Bridge }
}

/** In a plain browser (development preview) there is no bridge and no activation step. */
export const hasBridge = () => typeof window !== 'undefined' && !!window.icpc;
export const bridge = () => window.icpc!;

export function errorText(e: LicenseError | undefined, extra: { left?: number; detail?: string } = {}): string {
  switch (e) {
    case 'name': return 'Ismingizni kiriting (kamida 2 ta harf).';
    case 'not_configured': return 'Bu nusxada faollashtirish sozlanmagan. Ilovani administrator yigʻgan oʻrnatuvchidan oʻrnating.';
    case 'cooldown': return 'Yangi kodni bir daqiqadan keyin soʻrash mumkin.';
    case 'network': return 'Telegramga ulanib boʻlmadi. Internetni tekshirib, qayta urinib koʻring.';
    case 'telegram': return `Telegram kodni qabul qilmadi${extra.detail ? ` (${extra.detail})` : ''}. Administratorga xabar bering.`;
    case 'no_code': return 'Avval "Kod yuborish" tugmasini bosing.';
    case 'expired': return 'Kod muddati tugadi. Yangi kod soʻrang.';
    case 'format': return 'Kod 6 ta raqamdan iborat.';
    case 'wrong': return `Kod notoʻgʻri. Yana ${extra.left ?? 0} ta urinish qoldi.`;
    case 'too_many': return 'Juda koʻp notoʻgʻri urinish. Bu kod bekor qilindi — yangisini soʻrang.';
    default: return 'Nimadir xato ketdi. Qayta urinib koʻring.';
  }
}
