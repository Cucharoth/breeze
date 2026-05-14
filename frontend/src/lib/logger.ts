const IS_PROD = process.env.NEXT_PUBLIC_IS_PROD === 'true';

export const logger = {
  debug: (...args: any[]) => {
    if (!IS_PROD) {
      console.log('%cDEBUG:', 'color: #7f8c8d; font-weight: bold;', ...args);
    }
  },
  info: (...args: any[]) => {
    console.log('%cINFO:', 'color: #3498db; font-weight: bold;', ...args);
  },
  warn: (...args: any[]) => {
    console.log('%cWARN:', 'color: #f39c12; font-weight: bold;', ...args);
  },
  error: (...args: any[]) => {
    console.log('%cERROR:', 'color: #e74c3c; font-weight: bold;', ...args);
  }
};
