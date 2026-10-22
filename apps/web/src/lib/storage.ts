/**
 * Storage adapter. The personal build keeps everything in the browser.
 * When the app is published later, add e.g. an HTTP adapter (FastAPI + Postgres)
 * with the same interface and swap `activeStorage` (see docs/DESIGN.md section 11).
 */
export interface StorageAdapter {
  getItem(key: string): string | null | Promise<string | null>;
  setItem(key: string, value: string): void | Promise<void>;
  removeItem(key: string): void | Promise<void>;
}

const memory = new Map<string, string>();

export const localStorageAdapter: StorageAdapter = {
  getItem(key) {
    try {
      return window.localStorage.getItem(key);
    } catch {
      return memory.get(key) ?? null;
    }
  },
  setItem(key, value) {
    try {
      window.localStorage.setItem(key, value);
    } catch {
      memory.set(key, value);
    }
  },
  removeItem(key) {
    try {
      window.localStorage.removeItem(key);
    } catch {
      memory.delete(key);
    }
  },
};

export const activeStorage: StorageAdapter = localStorageAdapter;

export const PROGRESS_KEY = "pyai-progress";
