
let flag = true;

function toggleMenu(x) {
  x.classList.toggle("change");
  if(flag===true) {
    flag = false;
    document.getElementById("overlay-menu-div").style.width = "100%";
  } else {
    document.getElementById("overlay-menu-div").style.width = "0%";

    flag = true;
  };
};

function myAlert(val) {
  if (confirm("Sure you want to delete " + val)) {
    return true;
  } else {
    return false;
  }
};

let flagNav = true;

function toggleDropdown(x) {
  x.classList.toggle("change-dropdown");
  if(flagNav===true) {
    flagNav = false;
    document.getElementById("dropdown-content").style.display = "block";
  } else {
    document.getElementById("dropdown-content").style.display = "none";

    flagNav = true;
  };
};