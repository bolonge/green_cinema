window.addEventListener("scroll", (e) => {
  if (window.pageYOffset > 75) {
    document
      .querySelector("#nav")
      .classList.replace("header-transparent", "header-black");
  } else {
    document
      .querySelector("#nav")
      .classList.replace("header-black", "header-transparent");
  }
});
