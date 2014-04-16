$(function() {
  var $demo, tour;
  $demo = $("#demo");
  tour = new Tour({
    onStart: function() {
      return $demo.addClass("disabled", true);
    },
    onEnd: function() {
      return $demo.removeClass("disabled", true);
    },
    debug: true,
    steps: [
      {
        path: "/",
        element: "#demo",
        placement: "top",
        title: "Welcome to Website Tour!",
        content: "Learn to use the website by walking through the tour step by step."
      }, {
        path: "/",
        element: "#navbar",
        placement: "bottom",
        title: "Navigation Bar",
        content: "This is navigation bar. You can navigate the website by selecting a menu from this bar.",
        onHidden: function() {
            return window.location.assign("/");
        }
      }, {
        path: "/",
        element: "#login",
        placement: "bottom",
        title: "Login Form",
        content: "This is login form. Enter your credential here to access the administrator page.",
        onHidden: function() {
            return window.location.assign("/");
        }
      }, {
        path: "/statistics",
        title: "Statistic Summary",
        content: "This page illustrates the summary of publications and authors data.<br><br>" +
            "You can visit this page by selecting <small><b>Summary > Publication Summary</b></small> menu from the Navigation Bar.",
        orphan: true,
        onHidden: function() {
            return window.location.assign("/");
        }
      }, {
        path: "/statisticsdetails/author_statistics",
        title: "Author Statistic Page",
        content: "This table represents the statistic of all author. " +
            "You can sort each column in any order, filter the data by providing search key, " +
            "or change the number of item displayed per page.<br><br>" +
            "You can visit this page by selecting <small><b>Statistic Details > Author Statistics</b></small> menu from the Navigation Bar.",
        orphan: true,
        onHidden: function() {
            return window.location.assign("/");
        }
      }, {
        path: "/author_profile/Stefano%20Ceri",
        element: "#statistics",
        placement: "top",
        title: "Author Profile Page",
        content: "This page consist of 2 tabs. First tab shows the statistics of 1 particular author.<br><br>" +
            "You can visit this page by clicking any hyperlink on author name or from search result.",
        onShow: function() {
            $('#myTab a:first').tab('show')
        }
      }, {
        path: "/author_profile/Stefano%20Ceri",
        element: "#publications",
        placement: "top",
        title: "Author Profile Page",
        content: "Second tab shows list of publications in cronological order in the form of timeline.<br><br>" +
            "You can visit this page by clicking any hyperlink on author name or from search result.",
        onShow: function() {
            $('#myTab a:last').tab('show')
        }
      }, {
        path: "/search",
        element: "#searchbox",
        placement: "bottom",
        title: "Search Page",
        content: "If you want to find any author, you can use this search form. Enter an author name and click search.<br><br>" +
            "You can visit this page by selecting <small><b>Search Author</b></small> menu from the Navigation Bar.",
        onHidden: function() {
            return window.location.assign("/");
        }
      }, {
        path: "/network",
        title: "Publication Network",
        content: "This page shows the publication network within authors.<br><br>" +
            "You can visit this page by selecting <small><b>Publication Network</b></small> menu from the Navigation Bar.",
        orphan: true,
        onHidden: function() {
            return window.location.assign("/");
        }
      }, {
        path: "/about",
        element: "#contactform",
        placement: "top",
        title: "Contact Form",
        content: "If you have any questions or suggestions, you can send them using the provided contact form.<br><br>" +
            "You can access this form by clicking <small><b>Jeffries Team</b></small> hyperlink on page footer.",
        onHidden: function() {
            return window.location.assign("/");
        }
      }
    ]
  }).init().start();

  $(document).on("click", "[data-demo]", function(e) {
    e.preventDefault();
    if ($(this).hasClass("disabled")) {
      return;
    }
    tour.restart();
    return $(".alert").alert("close");
  });
});
