import express from 'express';
import { checkout } from '../controllers/checkoutController.js';
import { transactionApproved } from '../controllers/transactionApprovedController.js';
import { transactions } from '../controllers/transactionsController.js';
import {CheckOutPath, TransactionApprovedPath, TransactionsPath} from "../configs/pathsConfig.js";

const router = express.Router();

router.post(CheckOutPath, checkout);
router.post(TransactionApprovedPath, transactionApproved);
router.post(TransactionsPath, transactions);

export default router;
