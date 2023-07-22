import React, { useState, useEffect } from "react";
import './navbar.scss';
import { HiOutlineMenu } from "react-icons/hi";
import { Link, NavLink } from "react-router-dom";

const Navbar = () => {
    const [scroll, setScroll] = useState(false);
    const [offcanvasOpen, setOffcanvasOpen] = useState(false);

    const toggleOffcanvas = () => {
        setOffcanvasOpen(!offcanvasOpen);
    };
    useEffect(() => {
        window.addEventListener("scroll", () => {
            setScroll(window.scrollY > 50);
        });
    }, []);
    return (
        <>
        <nav className={scroll ? "navbar navbar-expand-lg navScroll" : "navbar navbar-expand-lg"}>
            <div className="container">
                <Link className="logo" to={`/`}>
                    <img src="/images/logo3.png" alt="logo" />
                </Link>
                <button className="navbar-toggler d-lg-none ms-auto pe-0" type="button" onClick={toggleOffcanvas}>
                   <HiOutlineMenu/>
                </button>

                <div className={`navbarOffset ms-auto ${offcanvasOpen ? "show" : ""}`}>
                    <div className="offset-header">
                        <h5 className="offcanvas-title" >
                            <img src="/images/logo3.png" alt="logo" height={30}/>
                         </h5>
                        <button type="button" className="btn-close" onClick={toggleOffcanvas} ></button>
                    </div>
                    <div className="d-lg-flex align-items-center gap-4">
                        <ul className="nav_list">
                            <li className="nav-item">
                                <NavLink to={`/`} className={({ isActive, isPending }) => isPending ? "pending" : isActive ? "nav-link active" : "nav-link" } onClick={toggleOffcanvas}>
                                    Home
                                </NavLink>
                            </li>
                            <li className="nav-item">
                                <NavLink to={`/about`} className={({ isActive, isPending }) => isPending ? "pending" : isActive ? "nav-link" : "nav-link" } onClick={toggleOffcanvas}>
                                    About
                                </NavLink>
                            </li>
                            <li className="nav-item">
                                <NavLink to={`/payment`} className={({ isActive, isPending }) => isPending ? "pending" : isActive ? "nav-link" : "nav-link" } onClick={toggleOffcanvas}>
                                    Contact
                                </NavLink>
                            </li>
                        </ul>
                        <div className="nav-btn d-flex gap-3">
                            <a href={`/address`} className='btn-lg'>Buy USDT</a>
                        </div>
                    </div>
                </div>

                <div className={`${offcanvasOpen ? "show offcanvas-backdrop fade" : ""}`} onClick={toggleOffcanvas}></div>
            </div>
        </nav>
        </>
    );
}

export default Navbar