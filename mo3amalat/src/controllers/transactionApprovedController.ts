import moamalat from '../configs/moamalatConfig';
import {validateCheckoutInput, ReferenceSchema} from '../middlewares/validation';
import { Request, Response } from 'express';

export const transactionApproved = async (req: Request, res: Response): Promise<void> => {
  validateCheckoutInput(ReferenceSchema, req, res, () => {
    const { error, value } = ReferenceSchema.validate(req.body);
    if (error) {
      res.status(400).json({ error: error.details });
      return;
    }

    const { amount, reference, date } = value;
    const result = moamalat.checkout(amount, reference, date);
    res.json(result);
  });
};
