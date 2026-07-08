class DocumentService:

    def get_documents(self):

        return [
            {
                "id": 1,
                "filename": "employee_handbook.pdf",
                "status": "uploaded"
            },
            {
                "id": 2,
                "filename": "vpn_guide.pdf",
                "status": "uploaded"
            }
        ]