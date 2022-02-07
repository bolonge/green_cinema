function go_profile_list(e) {
  if (e.innerHTML === "프로필") {
    document.querySelector("#my_profile").classList.replace("d-none", "d-flex");
    document
      .querySelector("#my_movie_list")
      .classList.replace("d-flex", "d-none");
  } else if (e.innerHTML === "내가 평가한 영화") {
    document.querySelector("#my_profile").classList.replace("d-flex", "d-none");
    document
      .querySelector("#my_movie_list")
      .classList.replace("d-none", "d-flex");
  }
}
