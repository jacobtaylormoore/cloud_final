boats = "boats"
# app_url = "https://mooreja2-rest.uc.r.appspot.com"
app_url = "http://localhost:8080"
json = "application/json"
html = "text/html"


# {
#     'resourceName': 'people/116677886026550631182',
#     'etag': '%EgUBAi43PRoEAQIFByIMRytZb3JnT1ZHZlk9',
#     'names': [{
#         'metadata': {
#             'primary': True,
#             'source': {
#                 'type': 'PROFILE',
#                 'id': '116677886026550631182'
#             },
#             'sourcePrimary': True
#         },
#         'displayName': 'Jake Moore',
#         'familyName': 'Moore',
#         'givenName': 'Jake',
#         'displayNameLastFirst': 'Moore, Jake',
#         'unstructuredName': 'Jake Moore'
#     }]
# }

test_jwt = {
    "access_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9tb29yZWphMi1qd3QudXMuYXV0aDAuY29tLyJ9..VYCXDXoiJC4Dxtuf.K2hHitNiCE3kcar9UxLXEj22LbZGstpWro5TSsib3j5txkPS3zr0-UxNnSfu9Ag4LJdv-QWDlyiqYsS870F7CCFWVlu7HiGFnQPXhrnmm2SK2v58T7Ey8IS7XnqamrZFqLeswWlGzQhiVZbUmUoEnF7WL_gK_lya4d4Azd3cYEr2Pz53tX93O7htytJ5zd8m3Rbd-rA_1CqucXCQztGCh7WJC3qkxgvhBkO8CowefTj-8m9i4WHokBpinSYfi9wJukNS3ui_BDMDlWK8_fTCygzL2S7B6fB_ltmeeItFnKApdmviol0pxY4QN1WOKJ3XVGQUQi9_VMYHf4-kACDPx_H0bTwTB4cXdt3pnXxZCI81.2A_iW0tvGltd7FmI5efmLA",
    "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhmNmZqOHl1bFdiMGxCX1dwVVBIaiJ9.eyJuaWNrbmFtZSI6InRlc3QxMjM0IiwibmFtZSI6InRlc3QxMjM0QHRlc3QuY29tIiwicGljdHVyZSI6Imh0dHBzOi8vcy5ncmF2YXRhci5jb20vYXZhdGFyLzAzZTc4ZWQzYzM2NDk1OWJhNGFjYzdiZmY2MzM3NmE4P3M9NDgwJnI9cGcmZD1odHRwcyUzQSUyRiUyRmNkbi5hdXRoMC5jb20lMkZhdmF0YXJzJTJGdGUucG5nIiwidXBkYXRlZF9hdCI6IjIwMjMtMDUtMjJUMTk6Mjg6NTkuOTY1WiIsImVtYWlsIjoidGVzdDEyMzRAdGVzdC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOi8vbW9vcmVqYTItand0LnVzLmF1dGgwLmNvbS8iLCJhdWQiOiI5N2J5QzExQUI1UTFERmszV2dJOWc0bUlSMmNQRENtOSIsImlhdCI6MTY4NDc4MzczOSwiZXhwIjoxNjg0ODE5NzM5LCJzdWIiOiJhdXRoMHw2NDZhOGYyMDcwNjliODNhOTQxZmQ0YzYifQ.H-0Ieoksmpvb_tSKKSZnDUciYtso2ezIwSUeoHYCET_QFfMWAWaZ5TRHIjhAW5b3dTKuIec2yb1_5ea1F1RHb8dI0WmfZnkc0eHb6QA1eDth4VI3GSBIBfxsUUa9PNL0GJMwUz7779s7n_SqSb8nYqVpmD-AaJlYOVVFA40ZGJ4ns1Nd1DyNfeenAvmWfuFisNRYgj1GmqedKkvlmrzY9RaXlfOfldQgznKG97k5yE_Y8ql5oNWxwHUSwR8PBn5Z2Q5_9rZtUL5SEIbNpiPRBEQEBgYCmN2wNKR2cBiGMVUO86jvMaQKr-bgnvRf1gEudl81BSDpJE7wUG4Fh3pwdQ",
    "scope": "openid profile email address phone",
    "expires_in": 86400,
    "token_type": "Bearer"
}

test_translated = {
    "header": {
        "alg": "RS256",
        "typ": "JWT",
        "kid": "xf6fj8yulWb0lB_WpUPHj"
    },
    "payload": {
        "nickname": "test1234",
        "name": "test1234@test.com",
        "picture": "https://s.gravatar.com/avatar/03e78ed3c364959ba4acc7bff63376a8?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fte.png",
        "updated_at": "2023-05-22T19:28:59.965Z",
        "email": "test1234@test.com",
        "email_verified": False,
        "iss": "https://mooreja2-jwt.us.auth0.com/",
        "aud": "97byC11AB5Q1DFk3WgI9g4mIR2cPDCm9",
        "iat": 1684783739,
        "exp": 1684819739,
        "sub": "auth0|646a8f207069b83a941fd4c6"
    }
}

jake_jwt = {
    "access_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9tb29yZWphMi1qd3QudXMuYXV0aDAuY29tLyJ9..nPP9tySNMPq44n70.SqZUPsTVnIw3cL-7-0q0NVqzIU080Br33e9DAIibtLk6mwldO3y9ObWKKV8vLRX3oW27R9RyZZ78oAJUfo92-L00Wh8oU95jBVlVTloo7WQifwSNAlJazoSlzgQUKOofuMR1ykuFYhgRg7qpj2O8ZPu0oGy9n9ZPTemGpwIJiqzJ5cGKlD7WoZg6cRdcU6ROKhYbyEMxY-4gxDzasxwHs2Sx4mOYItrVng-DIFS-rzzwu-V8PvMCnsGHPYfmqsuqJBJByVm1qQBIT9FqDofaoJT5QNL15SgmDQixpIT02YmmviS2j3jsq6Tg3dOiF8dT5esTO3oiBJ9GdfMVWVqa_VT4DuOKDKIjPWQu8DP1zXUr.jWS7Ebbtup9_nWBhxz1fxA",
    "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhmNmZqOHl1bFdiMGxCX1dwVVBIaiJ9.eyJuaWNrbmFtZSI6ImphY29idGF5bG9ybW9vcmUiLCJuYW1lIjoiamFjb2J0YXlsb3Jtb29yZUBnbWFpbC5jb20iLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvZmNkNGFmNTM1M2I0ZjI0YTk4M2NlYmQzNzczYjNiODg_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZqYS5wbmciLCJ1cGRhdGVkX2F0IjoiMjAyMy0wNS0yMlQxOTozNjo1NS45MzlaIiwiZW1haWwiOiJqYWNvYnRheWxvcm1vb3JlQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczovL21vb3JlamEyLWp3dC51cy5hdXRoMC5jb20vIiwiYXVkIjoiOTdieUMxMUFCNVExREZrM1dnSTlnNG1JUjJjUERDbTkiLCJpYXQiOjE2ODQ3ODQyMTUsImV4cCI6MTY4NDgyMDIxNSwic3ViIjoiYXV0aDB8NjQ2YTgzYTk5MmU4M2MyZDE5MmY0M2UyIn0.VZ2zFL4seVyeZvvoFu1DAjVVahg4JGm1cjh3-hYDGpoJgzrW7zdqxq9hhF6FWm_eSOA6aOtf4VpucoCECkB67H2Y-PD7JayHVbVL1yp2QdR39ryLtwGvPH3b_Cb-_lnQ8cXr5nLJ9e2SkhGGfdiFinVrZvCOYBZIvg_QIVdsJFKJEce9a8ml5hiaALdBvqvXt6KdIPBYxs6o2BD9d35xlrvsPlLnZ5Bm2wHkb6_8bZFTTJ89KltIHt1SYGurKq_3361YH_PTU0FOS2I3XH_OfrMwt3-7DcmgOLGmAuOF4HTyALHEvkG31CsahmpdY1O2nr_gzqwhvQ4gLt76WyiZ7Q",
    "scope": "openid profile email address phone",
    "expires_in": 86400,
    "token_type": "Bearer"
}

jake_translated = {
    "header": {
        "alg": "RS256",
        "typ": "JWT",
        "kid": "xf6fj8yulWb0lB_WpUPHj"
    },
    "payload": {
        "nickname": "jacobtaylormoore",
        "name": "jacobtaylormoore@gmail.com",
        "picture": "https://s.gravatar.com/avatar/fcd4af5353b4f24a983cebd3773b3b88?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fja.png",
        "updated_at": "2023-05-22T19:36:55.939Z",
        "email": "jacobtaylormoore@gmail.com",
        "email_verified": True,
        "iss": "https://mooreja2-jwt.us.auth0.com/",
        "aud": "97byC11AB5Q1DFk3WgI9g4mIR2cPDCm9",
        "iat": 1684784215,
        "exp": 1684820215,
        "sub": "auth0|646a83a992e83c2d192f43e2"
    }
}
