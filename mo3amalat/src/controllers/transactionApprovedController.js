import moamalat from '../configs/moamalatConfig.js';
import { validateCheckoutInput, ReferenceSchema } from '../middlewares/inputValidation.js';


export const transactionApproved = async (req, res) => {
  const {error , value} = validateCheckoutInput.validate(ReferenceSchema, req.body);
  if (error) {
    res.status(400).json({ error: error.details });
    return;
  }
  const { reference } = value;
  const result = await moamalat.transactionApproved(reference);
  res.json({ approved: result });
};
