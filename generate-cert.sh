#!/bin/bash

# Generate CA key and certificate
openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 365 -key ca.key -subj "/CN=Admission Controller CA" -out ca.crt

# Generate server key and certificate signing request (CSR)
openssl genrsa -out server.key 2048
openssl req -new -key server.key -subj "/CN=az-balancing-webhook-svc.default.svc" -out server.csr

# Create a configuration file for the SSL certificate
cat > csr.conf <<EOF
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = az-balancing-webhook-svc
DNS.2 = az-balancing-webhook-svc.default
DNS.3 = az-balancing-webhook-svc.default.svc
EOF

# Generate the SSL certificate
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -extensions v3_req -extfile csr.conf

# Base64 encode the CA certificate
CA_BUNDLE=$(cat ca.crt | base64 | tr -d '\n')

echo "CA_BUNDLE: $CA_BUNDLE"