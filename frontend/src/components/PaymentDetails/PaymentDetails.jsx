import React, { useState } from 'react';
import './PaymentDetails.scss'

const ContactForm = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [message, setMessage] = useState('');

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

    const handleSubmit = (event) => {
        event.preventDefault();
        // Here you can add your form submission logic
    };

    return (
        <div className="payment-area">
            <div className="container">
                <div className="row">
                    <div className="col-lg-12">
                        <form onSubmit={handleSubmit} className='from-input row'>
                            <div className="h5">Contact Us</div>
                            <div className="mb-3 col-12">
                                <label htmlFor="name" className="form-label">Name</label>
                                <input type="text" className="form-control" id="name" placeholder="Enter your name" value={name} onChange={handleNameChange} required />
                            </div>
                            <div className="mb-3 col-12">
                                <label htmlFor="email" className="form-label">Email</label>
                                <input type="email" className="form-control" id="email" placeholder="Enter your email" value={email} onChange={handleEmailChange} required />
                            </div>
                            <div className="mb-3 col-12">
                                <label htmlFor="phoneNumber" className="form-label">Phone Number</label>
                                <input type="text" className="form-control" id="phoneNumber" placeholder="Enter your phone number" value={phoneNumber} onChange={handlePhoneNumberChange} required />
                            </div>
                            <div className="mb-3 col-12">
                                <label htmlFor="message" className="form-label">Message</label>
                                <textarea className="form-control textarea" id="message" placeholder="Enter your message" value={message} onChange={handleMessageChange} required />
                            </div>
                            <div className="mt-5 col-md-6">
                                <button className="btn-lg" type="submit">Send Message</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ContactForm;
