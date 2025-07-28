schema_cyber = {
    "fields": {
        "MailDate": {
            "description": "Captures full date-time string following 'Sent:",
            "required": True,
            "mandatory": True
        },
        "RefNo": {
            "description": "Right-aligned value following the label 'Acknowledgement No.' Matches numeric acknowledgement number after label, allowing optional colon or dash",
            "required": True,
            "mandatory": True
        },
        "Police_Station_Address": {
            "description": "Captures uppercase address string and 'State /District /Police Station' string or may be number or alphanumeric string also.",
            "required": True,
            "mandatory": True
        },
        "Address": {
            "description": "Captures Right-aligned value following the label Address.It may be numeric or alphanumeric string.",
            "required": True,
            "mandatory": True
        },
        "Name": {
            "description": "Captures Right-aligned value following the label Name.",
            "required": True,
            "mandatory": True
        },
        "Mobile": {
            "description": "Captures Right-aligned value following the label Mobile.",
            "required": True,
            "mandatory": True
        },
        "Email": {
            "description": "Captures Right-aligned value following the label Email.",
            "required": True,
            "mandatory": True
        },
        "Total_Fraudulant_Amount": {
            "description": "Captures Right-aligned value following the label 'Total Fraudulent Amount reported by complainant'.",
            "required": True,
            "mandatory": True
        },

        "LineItems": {
            "description": "Extract all distinct itemized entries from the pdf compulsorily, ensuring no line item is missed and aligned with its serial number. This includes capturing every single line item present, regardless of page breaks or table continuations. Each row must represent one distinct item entry with its associated details, and the extraction process should handle multi-page tables seamlessly to maintain the integrity of individual entries. However, any line items that represent summation values, such as 'total goods', 'total allied services', or similar summations of other line items, must not be extracted alongside the distinct itemized entries. It should exclude summative rows to avoid duplication or misrepresentation.",
            "mandatory": True,
            "required": True,
            "type": "array",
            "items": {
                "type": "object",
                "properties": {

                    "ComplaintDate": {
                        "description": "Matches date and time in DD/MM/YYYY HH:MM:AM/PM format",
                        "type": "string",
                        "maxLength": 30,
                        "multiline": True,
                        "required": True,
                        "mandatory": True
                    },
                    "Amount": {
                        "description": "Text following the label 'Disputed' within the 'Amount' column, Captures numeric value after the word 'Disputed' (with or without colon or dash)",
                        "type": "string",
                        "maxLength": 30,
                        "multiline": True,
                        "required": True,
                        "mandatory": True
                    },
                    "Account_No": {
                        "description": "Extracts the first number (6–20 digits) before 'Layer' in 'Account No./(Wallet/PG/PA) Id' ",
                        "type": "string",
                        "maxLength": 200,
                        "multiline": True,
                        "required": True,
                        "mandatory": True
                    },
                    "Region": {
                        "description": "Captures uppercase state name from the cell beneath the label 'Complaint Reported By State'",
                        "type": "string",
                        "maxLength": 200,
                        "multiline": True,
                        "required": True,
                        "mandatory": True
                    },
                    "Utr_No": {
                        "description": "Captures alphanumeric UTR or transaction ID following the label 'Transaction Id / UTR Number'",
                        "type": "string",
                        "maxLength": 200,
                        "multiline": True,
                        "required": True,
                        "mandatory": True
                    },
                    "Utr_Amount": {
                        "description": "Extracts the numeric transaction amount following the 'Transaction :' label",
                        "type": "string",
                        "maxLength": 200,
                        "multiline": True,
                        "required": True,
                        "mandatory": True
                    },
                    "Transaction_Date": {
                        "description": "Captures date and time in DD/MM/YYYY and 12-hour time format, beneath the label 'Transaction Date'",
                        "type": "string",
                        "maxLength": 200,
                        "multiline": True,
                        "required": True,
                        "mandatory": True
                    },


                }
            }
        }
    }
}
