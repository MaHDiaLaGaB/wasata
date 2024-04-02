import React, { useState } from 'react';
import './PaymentDetails.scss';
import axios from 'axios';

const ContactForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [message, setMessage] = useState('');
  const [formErrors, setFormErrors] = useState({});
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePhoneNumberChange = (event) => {
    const cleanedValue = event.target.value.replace(/\D/g, '');
    setPhoneNumber(cleanedValue);
  };

  const handleMessageChange = (event) => {
    setMessage(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }
    try {
      const response = await axios.post(process.env.BACKEND_URL + '/api/v1/contact', {
        name,
        email,
        phone_number: phoneNumber,
        message,
      });
      console.log(response.data);
      // display success message to user
      setShowSuccessMessage(true);
      resetForm();
    } catch (error) {
      console.log(error);
      // display error message to user
    }
  };

  const validateForm = () => {
    const errors = {};
    if (!name) {
      errors.name = 'Please enter your name';
    }
    if (!email) {
      errors.email = 'Please enter your email';
    } else if (!isValidEmail(email)) {
      errors.email = 'Please enter a valid email address';
    }
    if (!phoneNumber) {
      errors.phoneNumber = 'Please enter your phone number';
    } else if (!isValidPhoneNumber(phoneNumber)) {
      errors.phoneNumber = 'Please enter a valid phone number';
    }
    if (!message) {
      errors.message = 'Please enter a message';
    }
    return errors;
  };

  const isValidEmail = (value) => {
    const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
    return emailRegex.test(value);
  };

  const isValidPhoneNumber = (value) => {
    const phoneRegex = /^\d{10}$/;
    return phoneRegex.test(value);
  };

  const resetForm = () => {
    setShowSuccessMessage(false);
    setName('');
    setEmail('');
    setPhoneNumber('');
    setMessage('');
    setFormErrors({});
  };

  return (
    <div className="payment-area">
      <div className="container">
        <div className="row">
          <div className="col-lg-12">
            <form onSubmit={handleSubmit} className="from-input row">
              <div className="h5">Contact Us</div>
              {showSuccessMessage && (
                <div className="alert alert-success" role="alert">
                  Your message has been sent successfully!
                </div>
              )}
              <div className={`mb-3 col-12 ${formErrors.name && 'has-error'}`}>
                <label htmlFor="name" className="form-label">
                  Name
                </label>
                <input
                  type="text"
                  className={`form-control ${formErrors.name && 'is-invalid'}`}
                  id="name"
                  placeholder="Enter your name"
                  value={name}
                  onChange={handleNameChange}
                  required
                />
                {formErrors.name && (
                  <div className="invalid-feedback">{formErrors.name}</div>
                )}
              </div>
              <div className={`mb-3 col-12 ${formErrors.email && 'has-error'}`}>
                <label htmlFor="email" className="form-label">
                  Email
                </label>
                <input
                  type="email"
                  className={`form-control ${formErrors.email && 'is-invalid'}`}
                  id="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={handleEmailChange}
                  required
                  pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
                />
                {formErrors.email && (
                  <div className="invalid-feedback">{formErrors.email}</div>
                )}
              </div>
              <div
                className={`mb-3 col-12 ${
                  formErrors.phoneNumber && 'has-error'
                }`}
              >
                <label htmlFor="phoneNumber" className="form-label">
                  Phone Number
                </label>
                <input
                  type="tel"
                  className={`form-control ${
                    formErrors.phoneNumber && 'is-invalid'
                  }`}
                  id="phoneNumber"
                  placeholder="Enter your phone number"
                  value={phoneNumber}
                  onChange={handlePhoneNumberChange}
                  required
                  pattern="[0-9]{10}"
                />
                {formErrors.phoneNumber && (
                  <div className="invalid-feedback">{formErrors.phoneNumber}</div>
                )}
              </div>
              <div className={`mb-3 col-12 ${formErrors.message && 'has-error'}`}>
                <label htmlFor="message" className="form-label">
                  Message
                </label>
                <textarea
                  className={`form-control textarea ${formErrors.message && 'is-invalid'}`}
                  id="message"
                  placeholder="Enter your message"
                  value={message}
                  onChange={handleMessageChange}
                  required
                />
                {formErrors.message && (
                  <div className="invalid-feedback">{formErrors.message}</div>
                )}
              </div>
              <div className="mt-5 col-md-6">
                <button className="btn-lg" type="submit">
                  Send Message
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactForm;