import moamalat from '../configs/moamalatConfig.js';

export const transactions = async (req, res) => {
  const { reference, options } = req.body;
  const result = await moamalat.transactions(reference, options);
  res.json(result);
};
