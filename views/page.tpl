<form action="/upload" method="post" enctype="multipart/form-data">
	<label for="email">Enter email address to get results</label>
	<input type="email" id="email" name="email" autocomplete="on" /><span style="color:red"> {{email_error or ''}}</span><br><br>

	<label for="upload">Select a file with sizes (<a href="/scrape/source-file-template">template</a>, 
		fill in as explained in <a href="https://github.com/fridgelord/tyre-price-scraping#usage">this table</a>):</label><br>
	<input type="file" id="upload" name="upload" accept=".xlsx" /><span style="color:red"> {{file_error or ''}}</span><br><br>

	Select source:<br>
	<input type="checkbox" id="platformaopon" name="platformaopon" />
	<label for="platformaopon">Platforma Opon</label><br>
	<input type="checkbox" id="oponeo" name="oponeo" />
	<label for="oponeo">Oponeo</label><br>
	<input type="checkbox" id="sklepopon" name="sklepopon" />
	<label for="sklepopon">SklepOpon</label><br>
	<input type="checkbox" id="intercars" name="intercars" />
	<label for="intercars">Inter Cars</label><br><br>

	<input type="submit" value="Scrape data" />
</form>

