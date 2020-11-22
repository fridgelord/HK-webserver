<!DOCTYPE html>
<html lang="en">

<head>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>Hankook Tire Polska</title>

  <!-- Bootstrap core CSS -->
  <link href="static/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

</head>

<body>

  <!-- Navigation -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
    <div class="container">
      <!-- <a class="navbar-brand" href="#">Start Bootstrap</a> */ -->
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarResponsive">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#top">Top
              <span class="sr-only">(current)</span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#Price Scraping">Price Scraping</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- Page Content -->
  <div class="container">

    <div class="row align-items-center"> 
      <div id="Price Scraping" class="col-6" >
        <!-- <h1 class="mt-5">A Bootstrap 4 Starter Template</h1> -->
        <!-- <p class="lead">Complete with pre-defined file paths and responsive navigation!</p> -->
        <!-- <ul class="list-unstyled"> -->
        <!--   <li>Bootstrap 4.5.3</li> -->
        <!--   <li>jQuery 3.5.1</li> -->
        <!-- </ul> -->
        <h1 style="text-align:center">Price Scraping</h1>
        <p>
        <form action="/upload" method="post" enctype="multipart/form-data">
          <div class="form-group">
            <label for="email" class="control-label">Enter email address to get results:</label>
            <input type="email" id="email" class="form-control" name="email" autocomplete="on" /><span style="color:red"> {{email_error or ''}}</span><br><br>
          </div>
          <div class="form group">
            <label for="upload">Select a file with sizes (<a href="/scrape/source-file-template">template</a>, 
                    fill in as explained in <a href="https://github.com/fridgelord/tyre-price-scraping#usage">this table</a>):</label><br>
            <input type="file" id="upload" class="form-control-file" name="upload" accept=".xlsx" /><span style="color:red"> {{file_error or ''}}</span>
          </div>
          <div class="form group">
            <b><p>Select source(s):</p></b>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" id="platformaopon" name="platformaopon" />
              <label for="platformaopon">Platforma Opon</label><br>
              <input class="form-check-input" type="checkbox" id="oponeo" name="oponeo" />
              <label for="oponeo">Oponeo</label><br>
              <input class="form-check-input" type="checkbox" id="sklepopon" name="sklepopon" />
              <label for="sklepopon">SklepOpon</label><br>
              <input class="form-check-input" type="checkbox" id="intercars" name="intercars" />
              <label for="intercars">Inter Cars</label><br><br>
            <div/>
          <div/>
            <input type="submit" value="Scrape data" />
        </form>
        </p>
      </div>
    </div>

  </div>

  <!-- Bootstrap core JavaScript -->
  <script src="static/vendor/jquery/jquery.slim.min.js"></script>
  <script src="static/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

</body>

</html>
