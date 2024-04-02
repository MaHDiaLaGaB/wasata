import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import './AddressForm.scss'
import axios from 'axios';

const AddressForm = () => {
  const { register, handleSubmit, formState: { errors }, reset } = useForm();
  const [submitting, setSubmitting] = useState(false);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);

  const onSubmit = async (data) => {
    setSubmitting(true);
    const url = process.env.BACKEND_URL + '/api/v1/buy'; // replace YOUR_PORT with the actual port number

    const requestData = {
      phone_number: data.phone.toString(),
      tokens: parseFloat(data.amount.toString())
    };

    const params = new URLSearchParams({
      admin_username: 'osama', // replace with actual admin username
      wallet_address: data.wallet // replace with actual wallet address
    });

    try {
      const response = await axios.post(`${url}?${params}`, requestData);
      console.log(response.data);
      setShowSuccessMessage(true);
      setSubmitting(false);
      resetForm();
    } catch (error) {
      console.error('Error:', error);
      setSubmitting(false);
    } finally {
            setSubmitting(false);
    }
  };

  const resetForm = () => {
    setShowSuccessMessage(false);
    reset();
  };

  return (
    <div className="address-area">
      <div className="container">
        <div className="row">
          <div className="col-lg-12">
            <form onSubmit={handleSubmit(onSubmit)} className='from-input'>
              {showSuccessMessage && (
                <div className="alert alert-success" role="alert">
                  Your message has been sent successfully!
                </div>
              )}
              <div className="mb-3">
                <label htmlFor="phone" className="form-label">Phone number</label>
                <input
                  className={`form-control ${errors.phone ? 'is-invalid' : ''}`}
                  type="text"
                  id="phone"
                  placeholder="Your Number"
                  {...register('phone', { required: 'Phone number is required' })}
                />
                {errors.phone && <div className="invalid-feedback">{errors.phone.message}</div>}
              </div>
              <div className="mb-3">
                <label htmlFor="wallet" className="form-label">Wallet address</label>
                <input
                  type="text"
                  className={`form-control ${errors.wallet ? 'is-invalid' : ''}`}
                  id="wallet"
                  placeholder="Your wallet address"
                  {...register('wallet', { required: 'Wallet address is required' })}
                />
                {errors.wallet && <div className="invalid-feedback">{errors.wallet.message}</div>}
              </div>
              <div className="mb-3">
                <label htmlFor="amount" className="form-label">USDT amount</label>
                <input
                  type="number"
                  className={`form-control ${errors.amount ? 'is-invalid' : ''}`}
                  id="amount"
                  placeholder="Your USDT amount"
                  {...register('amount', {
                    required: 'USDT amount is required',
                    min: { value: 10, message: 'USDT amount must be greater than 9' },
                    step: { value: 0.0001, message: 'USDT amount must be a multiple of 0.0001' }
                  })}
                />
                {errors.amount && <div className="invalid-feedback">{errors.amount.message}</div>}
              </div>
              <div className="pt-2">
                <button type="submit" className='btn-lg' disabled={submitting}>Next</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddressForm;
