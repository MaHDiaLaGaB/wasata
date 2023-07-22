import React from 'react';
import './hero.scss'

const Hero = () => {
    return (
        <div className="hero-area">
            <div className="container">
                <div className="row">
                    <div className="col-lg-6 align-self-center">
                        <div className="hero-text">
                            <h1>Learn, buy & sell crypto <span>easily and so fast</span> </h1>
                            <p>safest, and fastest way to buy & sell crypto asset exchange.</p>
                            <a href={`/address`} className="btn-lg">Buy USD</a>
                        </div>
                    </div>
                    <div className="col-lg-6 align-self-end">
                        <div className="hero-img">
                            <img className="hero1" src="/images/hero1.png" alt="hero images" />
                            <img className="hero2" src="/images/hero2.png" alt="hero images" />
                            <img className="hero3" src="/images/hero3.png" alt="hero images" />
                            <img className="hero4" src="/images/hero4.png" alt="hero images" />
                        </div>
                    </div>
                </div>
            </div>
        </div>

    )
}

export default Hero