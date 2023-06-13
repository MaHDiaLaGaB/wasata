import Moamalat from 'moamalat';

const moamalat = new Moamalat({
    merchantId: process.env.TEST_MO_MERCHANT_ID,
    terminalId: process.env.TEST_MO_TERMINAL_ID,
    secureKey: process.env.TEST_MO_SECURE_ID,
    prod: false,
});

export default moamalat;
