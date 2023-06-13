import moamalat from '../configs/moamalatConfig';
// import { CheckoutType } from '../configs/typesConfig'
import { validateCheckoutInput, checkoutSchema } from '../middlewares/validation';
import { Request, Response } from 'express';

export const checkout = async (req: Request, res: Response): Promise<void> => {
  validateCheckoutInput(checkoutSchema, req, res, () => {
    const { error, value } = checkoutSchema.validate(req.body);
    if (error) {
      res.status(400).json({ error: error.details });
      return;
    }

    const { amount, reference, date } = value;
    const result = moamalat.checkout(amount, reference, date);
    res.json(result);
  });
};
