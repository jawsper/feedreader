import { writable } from "svelte/store";
import type { IToast } from "../types";

interface IExpiringToast extends IToast {
  expiry: Date;
  context?: any;
}

interface ToastOptions {
  timeout?: number;
  context?: any;
}

const toast_expired = (expiry: Date) => {
  const now = new Date();
  return Math.abs(now.getTime() - expiry.getTime()) < 10
}

const makeToasts = () => {
  const { subscribe, update } = writable<IExpiringToast[]>([]);

  const expire_toasts = () => {
    update((toasts) => {
      return toasts.filter((toast) => toast_expired(toast.expiry));
    });
  };

  const push = (toast: IToast, options?: ToastOptions) => {
    const { timeout, context } = Object.assign(
      {},
      { timeout: 5000, context: null },
      options
    );
    const expiry = new Date(new Date().getTime() + timeout);
    const new_toast = { ...toast, expiry, context };

    update((current) => {
      if (context) {
        return [
          ...current.filter((toast) => toast.context !== context),
          new_toast,
        ];
      }
      return [...current, new_toast];
    });
    setTimeout(expire_toasts, timeout);
  };

  return {
    subscribe,
    push,
  };
};

export const toasts = makeToasts();
