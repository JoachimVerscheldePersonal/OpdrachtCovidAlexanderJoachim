(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[6218,7113],{92802:(r,e,n)=>{"use strict";n.d(e,{Z:()=>i});var t=n(94015);var s=n.n(t);var o=n(23645);var a=n.n(o);var c=a()(s());c.push([r.id,".cm-s-ssms span.cm-keyword { color: blue; }\n.cm-s-ssms span.cm-comment { color: darkgreen; }\n.cm-s-ssms span.cm-string { color: red; }\n.cm-s-ssms span.cm-def { color: black; }\n.cm-s-ssms span.cm-variable { color: black; }\n.cm-s-ssms span.cm-variable-2 { color: black; }\n.cm-s-ssms span.cm-atom { color: darkgray; }\n.cm-s-ssms .CodeMirror-linenumber { color: teal; }\n.cm-s-ssms .CodeMirror-activeline-background { background: #ffffff; }\n.cm-s-ssms span.cm-string-2 { color: #FF00FF; }\n.cm-s-ssms span.cm-operator, \n.cm-s-ssms span.cm-bracket, \n.cm-s-ssms span.cm-punctuation { color: darkgray; }\n.cm-s-ssms .CodeMirror-gutters { border-right: 3px solid #ffee62; background-color: #ffffff; }\n.cm-s-ssms div.CodeMirror-selected { background: #ADD6FF; }\n\n","",{version:3,sources:["webpack://./node_modules/codemirror/theme/ssms.css"],names:[],mappings:"AAAA,6BAA6B,WAAW,EAAE;AAC1C,6BAA6B,gBAAgB,EAAE;AAC/C,4BAA4B,UAAU,EAAE;AACxC,yBAAyB,YAAY,EAAE;AACvC,8BAA8B,YAAY,EAAE;AAC5C,gCAAgC,YAAY,EAAE;AAC9C,0BAA0B,eAAe,EAAE;AAC3C,oCAAoC,WAAW,EAAE;AACjD,+CAA+C,mBAAmB,EAAE;AACpE,8BAA8B,cAAc,EAAE;AAC9C;;iCAEiC,eAAe,EAAE;AAClD,iCAAiC,+BAA+B,EAAE,yBAAyB,EAAE;AAC7F,qCAAqC,mBAAmB,EAAE",sourcesContent:[".cm-s-ssms span.cm-keyword { color: blue; }\n.cm-s-ssms span.cm-comment { color: darkgreen; }\n.cm-s-ssms span.cm-string { color: red; }\n.cm-s-ssms span.cm-def { color: black; }\n.cm-s-ssms span.cm-variable { color: black; }\n.cm-s-ssms span.cm-variable-2 { color: black; }\n.cm-s-ssms span.cm-atom { color: darkgray; }\n.cm-s-ssms .CodeMirror-linenumber { color: teal; }\n.cm-s-ssms .CodeMirror-activeline-background { background: #ffffff; }\n.cm-s-ssms span.cm-string-2 { color: #FF00FF; }\n.cm-s-ssms span.cm-operator, \n.cm-s-ssms span.cm-bracket, \n.cm-s-ssms span.cm-punctuation { color: darkgray; }\n.cm-s-ssms .CodeMirror-gutters { border-right: 3px solid #ffee62; background-color: #ffffff; }\n.cm-s-ssms div.CodeMirror-selected { background: #ADD6FF; }\n\n"],sourceRoot:""}]);const i=c},23645:r=>{"use strict";r.exports=function(r){var e=[];e.toString=function e(){return this.map((function(e){var n=r(e);if(e[2]){return"@media ".concat(e[2]," {").concat(n,"}")}return n})).join("")};e.i=function(r,n,t){if(typeof r==="string"){r=[[null,r,""]]}var s={};if(t){for(var o=0;o<this.length;o++){var a=this[o][0];if(a!=null){s[a]=true}}}for(var c=0;c<r.length;c++){var i=[].concat(r[c]);if(t&&s[i[0]]){continue}if(n){if(!i[2]){i[2]=n}else{i[2]="".concat(n," and ").concat(i[2])}}e.push(i)}};return e}},94015:r=>{"use strict";function e(r,e){return a(r)||o(r,e)||t(r,e)||n()}function n(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}function t(r,e){if(!r)return;if(typeof r==="string")return s(r,e);var n=Object.prototype.toString.call(r).slice(8,-1);if(n==="Object"&&r.constructor)n=r.constructor.name;if(n==="Map"||n==="Set")return Array.from(r);if(n==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return s(r,e)}function s(r,e){if(e==null||e>r.length)e=r.length;for(var n=0,t=new Array(e);n<e;n++){t[n]=r[n]}return t}function o(r,e){var n=r&&(typeof Symbol!=="undefined"&&r[Symbol.iterator]||r["@@iterator"]);if(n==null)return;var t=[];var s=true;var o=false;var a,c;try{for(n=n.call(r);!(s=(a=n.next()).done);s=true){t.push(a.value);if(e&&t.length===e)break}}catch(i){o=true;c=i}finally{try{if(!s&&n["return"]!=null)n["return"]()}finally{if(o)throw c}}return t}function a(r){if(Array.isArray(r))return r}r.exports=function r(n){var t=e(n,4),s=t[1],o=t[3];if(typeof btoa==="function"){var a=btoa(unescape(encodeURIComponent(JSON.stringify(o))));var c="sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(a);var i="/*# ".concat(c," */");var u=o.sources.map((function(r){return"/*# sourceURL=".concat(o.sourceRoot||"").concat(r," */")}));return[s].concat(u).concat([i]).join("\n")}return[s].join("\n")}},26218:(r,e,n)=>{"use strict";n.r(e);n.d(e,{default:()=>i});var t=n(93379);var s=n.n(t);var o=n(92802);var a={};a.insert="head";a.singleton=false;var c=s()(o.Z,a);const i=o.Z.locals||{}},93379:(r,e,n)=>{"use strict";var t=function r(){var e;return function r(){if(typeof e==="undefined"){e=Boolean(window&&document&&document.all&&!window.atob)}return e}}();var s=function r(){var e={};return function r(n){if(typeof e[n]==="undefined"){var t=document.querySelector(n);if(window.HTMLIFrameElement&&t instanceof window.HTMLIFrameElement){try{t=t.contentDocument.head}catch(s){t=null}}e[n]=t}return e[n]}}();var o=[];function a(r){var e=-1;for(var n=0;n<o.length;n++){if(o[n].identifier===r){e=n;break}}return e}function c(r,e){var n={};var t=[];for(var s=0;s<r.length;s++){var c=r[s];var i=e.base?c[0]+e.base:c[0];var u=n[i]||0;var l="".concat(i," ").concat(u);n[i]=u+1;var f=a(l);var m={css:c[1],media:c[2],sourceMap:c[3]};if(f!==-1){o[f].references++;o[f].updater(m)}else{o.push({identifier:l,updater:p(m,e),references:1})}t.push(l)}return t}function i(r){var e=document.createElement("style");var t=r.attributes||{};if(typeof t.nonce==="undefined"){var o=true?n.nc:0;if(o){t.nonce=o}}Object.keys(t).forEach((function(r){e.setAttribute(r,t[r])}));if(typeof r.insert==="function"){r.insert(e)}else{var a=s(r.insert||"head");if(!a){throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.")}a.appendChild(e)}return e}function u(r){if(r.parentNode===null){return false}r.parentNode.removeChild(r)}var l=function r(){var e=[];return function r(n,t){e[n]=t;return e.filter(Boolean).join("\n")}}();function f(r,e,n,t){var s=n?"":t.media?"@media ".concat(t.media," {").concat(t.css,"}"):t.css;if(r.styleSheet){r.styleSheet.cssText=l(e,s)}else{var o=document.createTextNode(s);var a=r.childNodes;if(a[e]){r.removeChild(a[e])}if(a.length){r.insertBefore(o,a[e])}else{r.appendChild(o)}}}function m(r,e,n){var t=n.css;var s=n.media;var o=n.sourceMap;if(s){r.setAttribute("media",s)}else{r.removeAttribute("media")}if(o&&typeof btoa!=="undefined"){t+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(o))))," */")}if(r.styleSheet){r.styleSheet.cssText=t}else{while(r.firstChild){r.removeChild(r.firstChild)}r.appendChild(document.createTextNode(t))}}var A=null;var d=0;function p(r,e){var n;var t;var s;if(e.singleton){var o=d++;n=A||(A=i(e));t=f.bind(null,n,o,false);s=f.bind(null,n,o,true)}else{n=i(e);t=m.bind(null,n,e);s=function r(){u(n)}}t(r);return function e(n){if(n){if(n.css===r.css&&n.media===r.media&&n.sourceMap===r.sourceMap){return}t(r=n)}else{s()}}}r.exports=function(r,e){e=e||{};if(!e.singleton&&typeof e.singleton!=="boolean"){e.singleton=t()}r=r||[];var n=c(r,e);return function r(t){t=t||[];if(Object.prototype.toString.call(t)!=="[object Array]"){return}for(var s=0;s<n.length;s++){var i=n[s];var u=a(i);o[u].references--}var l=c(t,e);for(var f=0;f<n.length;f++){var m=n[f];var A=a(m);if(o[A].references===0){o[A].updater();o.splice(A,1)}}n=l}}}}]);
//# sourceMappingURL=6218.63a4725450fdf0562cd8.js.map?v=63a4725450fdf0562cd8