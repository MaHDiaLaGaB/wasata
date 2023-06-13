import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import router from './src/routes/routers.js';

require('dotenv').config();

const app = express();
const port = process.env.MOAMALAT_PORT;

// Apply security best practices
app.use(helmet());
app.use(cors()); // Configure CORS options as needed
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // limit each IP to 10 requests per windowMs
});
app.use(limiter);

// Routes
app.use(router);

// to avoid revealing information about the server
app.disable('x-powered-by');


app.listen(port, '0.0.0.0',() => {
  console.log(`Server listening at http://0.0.0.0:${port}`);
});
