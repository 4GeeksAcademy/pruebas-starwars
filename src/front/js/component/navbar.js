import React, { useContext, useEffect } from "react";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";

export const Navbar = () => {
    const { store, actions } = useContext(Context);
    console.log("Usuario en Navbar:", store.user);
    console.log("Token en Navbar:", store.token);

    const navigate = useNavigate();


    const handleLogout = () => {
        actions.logout();
        navigate("/");
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark border-bottom border-warning">
            <div className="container-fluid">
                <Link to="/" className="navbar-brand">
                    <img
                        src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Star_Wars_Logo.svg/1200px-Star_Wars_Logo.svg.png"
                        alt="Star Wars Logo"
                        width="100"
                        height="auto"
                        className="d-inline-block align-text-top"
                    />
                </Link>
                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse d-flex justify-content-between" id="navbarNav">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        {!store.token && (
                            <li className="nav-item">
                                <Link to="/login" className="nav-link text-warning">
                                    Login
                                </Link>
                            </li>
                        )}
                        <li className="nav-item">
                            <Link to="/signup" className="nav-link text-warning">
                                Signup
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/characters" className="nav-link text-warning">
                                Characters
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/starships" className="nav-link text-warning">
                                Starships
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/planets" className="nav-link text-warning">
                                Planets
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/contacts" className="nav-link text-warning">
                                Contacts
                            </Link>
                        </li>
                    </ul>

                    {store.user && (
                        <span className="text-warning me-3">Bienvenido, {store.user.first_name}</span>
                    )}

                    {store.token ? (
                        <button className="btn btn-outline-danger" onClick={handleLogout}>
                            Cerrar Sesión
                        </button>
                    ) : null}

                    <div className="dropdown ms-3">
                        <button
                            className="btn btn-outline-warning dropdown-toggle"
                            type="button"
                            id="favoritesDropdown"
                            data-bs-toggle="dropdown"
                            aria-expanded="false"
                        >
                            Favorites ({store.favorites.length})
                        </button>
                        <ul className="dropdown-menu dropdown-menu-end bg-dark border-warning" aria-labelledby="favoritesDropdown">
                            {store.favorites.map((fav) => (
                                <li key={fav.uid} className="d-flex align-items-center">
                                    <Link to={`/${fav.type}/${fav.uid}`} className="dropdown-item text-warning">
                                        {fav.name}
                                    </Link>
                                    <button
                                        className="btn btn-sm btn-outline-danger ms-2"
                                        onClick={() => actions.removeFavorite(fav.uid)}
                                    >
                                        🗑️
                                    </button>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </nav>
    );
};
