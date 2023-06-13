import Moamalat from 'moamalat';

interface MoamalatConfig {
  merchantId: string;
  terminalId: string;
  secureKey: string;
  prod: boolean;
}

const moamalatConfig: MoamalatConfig = {
  merchantId: process.env.TEST_MO_MERCHANT_ID!,
  terminalId: process.env.TEST_MO_TERMINAL_ID!,
  secureKey: process.env.TEST_MO_SECURE_ID!,
  prod: false,
};

const moamalat: Moamalat = new Moamalat(moamalatConfig);

export default moamalat;
