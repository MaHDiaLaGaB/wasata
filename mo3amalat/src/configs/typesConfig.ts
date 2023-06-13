export type CheckoutType = {
  MID: string;
  TID: string;
  AmountTrxn: number;
  MerchantReference: string;
  TrxDateTime: string;
  SecureHash: string;
};

export type Reference = string | number;
