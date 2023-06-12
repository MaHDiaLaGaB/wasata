import moamalat from '../configs/moamalatConfig.js';
// import { CheckoutType }from '../configs/typesConfig.js'
import { validateCheckoutInput, checkoutSchema } from '../middlewares/inputValidation.js';

export const checkout = async (req, res) => {
  const { error, value } = validateCheckoutInput.validate(checkoutSchema, req.body);
  if (error) {
    res.status(400).json({ error: error.details });
    return;
  }

  const { amount, reference, date } = value;
  const result = moamalat.checkout(amount, reference, date);
  res.json(result);
};
