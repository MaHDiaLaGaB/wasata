// validation.ts
import Joi, { ObjectSchema, ValidationResult } from 'joi';
import { Request, Response, NextFunction } from 'express';

export const checkoutSchema: ObjectSchema = Joi.object({
  amount: Joi.number().required(),
  reference: Joi.string().optional(),
  date: Joi.date().optional(),
});

export const ReferenceSchema: ObjectSchema = Joi.object({
  reference: Joi.alternatives().try(Joi.string().required(), Joi.number().required()),
});

export const validateCheckoutInput = (
  schema: ObjectSchema,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const validationResult: ValidationResult = schema.validate(req.body);
  const { error } = validationResult;
  if (error) {
    res.status(400).json({ error: error.details });
    return;
  }

  next();
};
