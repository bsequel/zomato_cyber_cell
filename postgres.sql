CREATE TABLE fraudComplaints (
    sNo SERIAL PRIMARY KEY,
    complaintDate VARCHAR(50),
    mailDate VARCHAR(50),
    mailMonth VARCHAR(50),
    amount VARCHAR(50),
    refNo VARCHAR(100),
    policeStationAddress VARCHAR(255),
    accountNo VARCHAR(100),
    name VARCHAR(100),
    mobileNumber VARCHAR(20),
    emailId VARCHAR(150),
    status VARCHAR(50),
    ageing VARCHAR(20),
    debitFromBank VARCHAR(10),
    region VARCHAR(100),
    utrNo VARCHAR(100),
    utrAmount VARCHAR(50),
    transactionDateTime VARCHAR(50),
    totalFraudulentAmount VARCHAR(50)
);
