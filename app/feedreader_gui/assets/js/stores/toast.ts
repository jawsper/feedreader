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

const makeToasts = () => {
  const { subscribe, update } = writable<IExpiringToast[]>([]);

  const expire_toasts = () => {
    const now = new Date();
    update((toasts) => {
      return toasts.filter((toast) => toast.expiry >= now);
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
      if (options.context) {
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
