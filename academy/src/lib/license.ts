/** Typed access to the Electron activation bridge (window.mirae). */

export interface LicenseStatus {
  configured: boolean;
  activated: boolean;
  /** A licence exists on this computer (it may be expired). */
  licensed?: boolean;
  expired?: boolean;
  /** The computer clock is earlier than a time the app already saw. */
  clockBack?: boolean;
  /** End of the one-year licence (ms). */
  validUntil?: number;
  daysLeft?: number;
  name: string;
  activatedAt: number;
  pending: boolean;
  expiresAt: number;
  resendAt: number;
}

export type LicenseError =
  | 'name' | 'not_configured' | 'cooldown' | 'network' | 'telegram'
  | 'no_code' | 'expired' | 'format' | 'wrong' | 'too_many' | 'clock';

export interface RequestResult { ok: boolean; error?: LicenseError; expiresAt?: number; resendAt?: number; retryAt?: number; detail?: string }
export interface VerifyResult { ok: boolean; error?: LicenseError; left?: number; name?: string; validUntil?: number }

interface Bridge {
  license: {
    status(): Promise<LicenseStatus>;
    request(name: string): Promise<RequestResult>;
    verify(code: string): Promise<VerifyResult>;
    rename(name: string): Promise<{ ok: boolean }>;
  };
  window?: {
    toggleFullscreen(): Promise<boolean>;
    isFullscreen(): Promise<boolean>;
    onFullscreen(cb: (v: boolean) => void): () => void;
  };
}

declare global {
  interface Window { mirae?: Bridge }
}

/** In a plain browser (development preview) there is no bridge and no activation step. */
export const hasBridge = () => typeof window !== 'undefined' && !!window.mirae;
export const bridge = () => window.mirae!;

const UZ_MONTHS = ['yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun', 'iyul', 'avgust', 'sentabr', 'oktabr', 'noyabr', 'dekabr'];
/** "13-oktabr 2027-yil" */
export const licenceDate = (ms: number) => {
  const d = new Date(ms);
  return `${d.getDate()}-${UZ_MONTHS[d.getMonth()]} ${d.getFullYear()}-yil`;
};

/** Days before the end when the app starts reminding about renewal. */
export const RENEW_WARN_DAYS = 30;

export function errorText(e: LicenseError | undefined, extra: { left?: number; detail?: string } = {}): string {
  switch (e) {
    case 'name': return 'Ismingizni kiriting (kamida 2 ta harf).';
    case 'not_configured': return 'Bu nusxada faollashtirish sozlanmagan. Ilovani Mirae Academy bergan oʻrnatuvchidan oʻrnating.';
    case 'cooldown': return 'Yangi kodni bir daqiqadan keyin soʻrash mumkin.';
    case 'network': return 'Telegramga ulanib boʻlmadi. Internetni tekshirib, qayta urinib koʻring.';
    case 'telegram': return `Telegram kodni qabul qilmadi${extra.detail ? ` (${extra.detail})` : ''}. Ustozingizga xabar bering.`;
    case 'no_code': return 'Avval "Kod yuborish" tugmasini bosing.';
    case 'expired': return 'Kod muddati tugadi. Yangi kod soʻrang.';
    case 'format': return 'Kod 6 ta raqamdan iborat.';
    case 'wrong': return `Kod notoʻgʻri. Yana ${extra.left ?? 0} ta urinish qoldi.`;
    case 'clock': return 'Kompyuter sanasi notoʻgʻri koʻrinadi. Sana va vaqtni toʻgʻrilab, ilovani qayta oching.';
    case 'too_many': return 'Juda koʻp notoʻgʻri urinish. Bu kod bekor qilindi — yangisini soʻrang.';
    default: return 'Nimadir xato ketdi. Qayta urinib koʻring.';
  }
}
