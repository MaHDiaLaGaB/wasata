import express, { Router, Request, Response } from 'express';
import { checkout } from '../controllers/checkoutController';
import { transactionApproved } from '../controllers/transactionApprovedController';
import { transactions } from '../controllers/transactionsController';
import { CheckOutPath, TransactionApprovedPath, TransactionsPath } from '../configs/pathsConfig';

const router: Router = express.Router();

router.post(CheckOutPath, checkout);
router.post(TransactionApprovedPath, transactionApproved);
router.post(TransactionsPath, transactions);

export default router;
