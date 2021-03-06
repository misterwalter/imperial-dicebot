echo

#Add bot_admin example token
if [ -e bot_admin ]

then 
	echo "bot_admin file exists, not overwriting"
else
	echo "Creating an example bot_admin file, replace the mention tag with your own."
	echo "<@!1234567890abcdefgh>" > bot_admin
fi

# Add token example file - there's no good way to 
if [ -e token ]
then 
	echo "token file exists, not overwriting"
else
	echo "Creating a token file, but you still need to add your bot's token!"
	echo "Put your bot's token, not their Client ID or Client secret, into this file, replacing this text." > token
fi

# Adds a default report_format file
if [ -e report_format ]
then 
	echo "report_format file exists, not overwriting"
else
	echo "Creating example report_format file. It requires no further effort"
	cat << EOF > report_format
{mention}'s performance for today:
    {successes} out of {dice} dice ({accuracy}%) on {rolls} rolls.
    You rolled an average of {efficiency} dice per roll.
EOF
fi

echo
