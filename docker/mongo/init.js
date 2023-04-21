db.createUser(
    {
        user: "mantium",
        pwd: "password",
        roles: [
            {
                role: "readWrite",
                db: "wordle"
            }
        ]
    }
);