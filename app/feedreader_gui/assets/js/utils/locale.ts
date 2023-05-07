import { enGB } from "date-fns/locale";

const baseLocale = enGB;

const formatRelative = (token: string, date: Date | number, baseDate: Date | number, options) => {
  if(token === "other") {
    return "P p";
  }
  return baseLocale.formatRelative(token, date, baseDate, options);
}

const locale = {
  ...baseLocale,
  formatRelative,
}

export { locale };
