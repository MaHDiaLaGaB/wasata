import Joi from 'joi';

export const checkoutSchema = Joi.object({
  amount: Joi.number().required(),
  reference: Joi.string().optional(),
  date: Joi.date().optional(),
});

export const ReferenceSchema = Joi.object({
  reference: Joi.string().required() | Joi.number().required()
});

export const validateCheckoutInput = (schema, req, res, next) => {
  const { error } = schema.validate(req.body);
  if (error) {
    res.status(400).json({ error: error.details });
    return;
  }

  next();
};
