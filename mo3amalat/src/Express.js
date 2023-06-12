// import express from 'express';
// import helmet from 'helmet';
// import cors from 'cors';
// import rateLimit from 'express-rate-limit';
// import Joi from 'joi';
// import Moamalat from 'moamalat'; // Import your TypeScript SDK
//
// const app = express();
// const port = 3000;
//
// const moamalat = new Moamalat(/* pass necessary parameters */);
//
// // Apply security best practices
// app.use(helmet());
// app.use(cors()); // Configure CORS options as needed
// app.use(express.json());
//
// // Rate limiting
// const limiter = rateLimit({
//   windowMs: 15 * 60 * 1000, // 15 minutes
//   max: 100, // limit each IP to 100 requests per windowMs
// });
// app.use(limiter);
//
// // Input validation schema
// const checkoutSchema = Joi.object({
//   amount: Joi.number().required(),
//   reference: Joi.string().optional(),
//   date: Joi.date().optional(),
// });
//
// // Routes
// app.post('/checkout', async (req, res) => {
//   const { error, value } = checkoutSchema.validate(req.body);
//   if (error) {
//     res.status(400).json({ error: error.details });
//     return;
//   }
//
//   const { amount, reference, date } = value;
//   const result = moamalat.checkout(amount, reference, date);
//   res.json(result);
// });
//
// app.post('/transactionApproved', async (req, res) => {
//   const { reference } = req.body;
//   const result = await moamalat.transactionApproved(reference);
//   res.json({ approved: result });
// });
//
// app.post('/transactions', async (req, res) => {
//   const { reference, options } = req.body;
//   const result = await moamalat.transactions(reference, options);
//   res.json(result);
// });
//
// app.listen(port, () => {
//   console.log(`Server listening at http://localhost:${port}`);
// });
