// app.ts
import express from 'express';
import { Express, RequestHandler } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import dotenv from 'dotenv';
import rateLimit from 'express-rate-limit';
import router from './routes/routers';

const result = dotenv.config();
if (result.error) {
  console.error('Error while loading .env file:', result.error);
}

const app: Express = express();
const port: string = process.env.MOAMALAT_PORT as string;
console.log(port);

// Apply security best practices
app.use(helmet());
app.use(cors()); // Configure CORS options as needed
app.use(express.json());

// Rate limiting
const limiter: RequestHandler = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // limit each IP to 10 requests per windowMs
});
app.use(limiter);

// Routes
app.use(router);

// to avoid revealing information about the server
app.disable('x-powered-by');

app.listen(Number(port), '0.0.0.0', () => {
  console.log(`Server listening at http://0.0.0.0:${port}`);
});
