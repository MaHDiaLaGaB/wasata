import moamalat from '../configs/moamalatConfig';
import { Request, Response } from 'express';

export const transactions = async (req: Request, res: Response): Promise<void> => {
  const { reference, options } = req.body;
  const result = await moamalat.transactions(reference, options);
  res.json(result);
};
