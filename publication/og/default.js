// deno:https://cdn.jsdelivr.net/gh/oscarotero/ssx@0.1.14/jsx-runtime.ts
var ssxElement = Symbol.for("ssx.element");
var voidElements = /* @__PURE__ */ new Set([
  "area",
  "base",
  "br",
  "col",
  "embed",
  "hr",
  "img",
  "input",
  "link",
  "meta",
  "param",
  "source",
  "track",
  "wbr"
]);
var attributes = /* @__PURE__ */ new Map([
  [
    "className",
    "class"
  ],
  [
    "htmlFor",
    "for"
  ]
]);
var proto = Object.create(null, {
  [ssxElement]: {
    value: true,
    enumerable: false
  },
  toString: {
    value: function() {
      return renderComponent(this);
    }
  }
});
function jsx(type, props) {
  const element = Object.create(proto);
  element.type = type;
  element.props = props;
  return element;
}
function Fragment(props) {
  return props.children;
}
async function jsxEscape(content) {
  if (isEmpty(content)) {
    return "";
  }
  if (Array.isArray(content)) {
    return (await Promise.all(content.map(jsxEscape))).join("");
  }
  switch (typeof content) {
    case "string":
      return content.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
    case "object":
      if ("__html" in content) {
        return content.__html ?? "";
      }
      if (isComponent(content)) {
        return await renderComponent(content);
      }
      break;
    case "number":
    case "boolean":
      return content.toString();
  }
  return content;
}
function isComponent(value) {
  return value !== null && typeof value === "object" && value[ssxElement] === true;
}
async function renderComponent(component) {
  if (Array.isArray(component)) {
    return (await Promise.all(component.map(renderComponent))).join("");
  }
  if (!isComponent(component)) {
    return await jsxEscape(component);
  }
  const { type, props } = component;
  if (type === Fragment) {
    return await jsxEscape(props.children);
  }
  if (typeof type === "string") {
    const isVoid = voidElements.has(type);
    const attrs = [
      type
    ];
    let content = "";
    if (props) {
      for (const [key, val] of Object.entries(props)) {
        if (key === "dangerouslySetInnerHTML") {
          content += val.__html ?? "";
          continue;
        }
        if (key === "children") {
          content += await jsxEscape(val);
          continue;
        }
        attrs.push(jsxAttr(key, val));
      }
    }
    if (isVoid) {
      if (content) {
        throw new Error(`Void element "${type}" cannot have children`);
      }
      return `<${attrs.join(" ")}>`;
    }
    return `<${attrs.join(" ")}>${content}</${type}>`;
  }
  if (typeof type !== "function") {
    throw new Error(`[SSX] Invalid component type: ${typeof type}. Expected a string or a function.`);
  }
  const comp = await type(props);
  return isEmpty(comp) ? "" : typeof comp === "string" ? comp : await renderComponent(comp);
}
function jsxAttr(name, value) {
  name = attributes.get(name) ?? name;
  if (name === "style" && typeof value === "object") {
    value = renderStyles(value);
  }
  if (isEmpty(value)) {
    return "";
  }
  if (value === true) {
    return name;
  }
  if (typeof value === "string") {
    return `${name}="${value.replaceAll('"', "&quot;")}"`;
  }
  if (typeof value === "number") {
    return `${name}="${value}"`;
  }
  console.warn(`[SSX] Unsupported value for attribute "${name}": (${typeof value}). Pass a string, number, or boolean.`);
  return "";
}
function renderStyles(properties) {
  return Object.entries(properties).filter(([, value]) => value !== void 0 && value !== null).map(([name, value]) => `${name}:${value};`).join("");
}
function isEmpty(value) {
  return value == null || value === void 0 || value === false;
}

// authored/_includes/open_graph/default.jsx
function default_default({ title, description, openGraphColor }) {
  if (!title) {
    title = "Deno documentation";
  }
  if (!description) {
    description = "Learn more at docs.deno.com";
  }
  return /* @__PURE__ */ jsx("div", {
    style: {
      width: "1200px",
      height: "630px",
      display: "flex",
      position: "relative",
      flexDirection: "column",
      justifyContent: "space-between",
      fontSize: 26,
      fontWeight: 400,
      textWrap: "balance",
      fontFamily: "Inter",
      backgroundColor: "#fff"
    },
    children: [
      /* @__PURE__ */ jsx("h1", {
        style: {
          margin: "0",
          fontSize: 64,
          fontWeight: 800,
          width: "100%",
          lineHeight: "1.1",
          letterSpacing: "-0.025em",
          position: "relative",
          backgroundColor: openGraphColor || "#70ffaf",
          padding: "20px 90px 0",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          height: "420px"
        },
        children: [
          title,
          /* @__PURE__ */ jsx("div", {
            style: {
              display: "block",
              fontSize: "21px",
              letterSpacing: "0",
              marginTop: "20px",
              borderTop: "2px solid #172723",
              paddingTop: "12px",
              width: "7.35em",
              fontWeight: 500,
              textWrap: "balance"
            },
            children: "docs.deno.com"
          })
        ]
      }),
      /* @__PURE__ */ jsx("div", {
        style: {
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          height: "230px",
          padding: "84px",
          border: `6px solid ${openGraphColor || "#70ffaf"}`
        },
        children: [
          /* @__PURE__ */ jsx("p", {
            style: {
              margin: 0,
              width: "720px",
              lineHeight: "1.5",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center"
            },
            children: description
          }),
          /* @__PURE__ */ jsx("svg", {
            xmlns: "http://www.w3.org/2000/svg",
            viewBox: "0 0 401 401",
            "fill-rule": "evenodd",
            style: {
              width: "80px",
              height: "80px"
            },
            children: /* @__PURE__ */ jsx("path", {
              d: "M261.684 245.149c33.861 1.662 69.225-13.535 80.203-43.776 10.978-30.241 6.721-60.148-32.661-78.086-39.381-17.944-57.569-39.272-89.385-52.14-20.787-8.408-43.915-3.418-67.664 9.707-63.963 35.351-121.274 147.038-94.858 250.518a3.185 3.185 0 0 1-1.544 3.615 3.189 3.189 0 0 1-3.877-.64C16.282 295.06-3.759 241.788.593 184.791 8.998 74.728 105.178-7.806 215.241.599 325.296 9.003 407.83 105.182 399.425 215.245c-3.529 46.221-22.535 87.584-51.559 119.399-22.195 22.8-50.473 32.935-74.07 32.516-17.107-.303-33.839-7.112-45.409-17.066-16.516-14.228-23.191-30.485-25.474-48.635-.572-4.507-.236-16.797 2.112-25.309 1.745-6.343 6.185-18.599 12.676-23.957-7.595-3.266-17.361-10.388-20.446-13.805-.753-.838-.652-2.156.026-3.057a2.56 2.56 0 0 1 2.925-.88c6.528 2.239 14.477 4.444 22.86 5.851 11.021 1.844 24.729 4.159 38.618 4.847ZM192.777 85.086c10.789-.846 20.202 8.363 21.825 20.609 2.164 16.314-3.822 33.166-23.511 33.554-16.819.335-21.915-16.625-20.8-26.9 1.107-10.275 9.577-26.25 22.486-27.263Z"
            })
          })
        ]
      })
    ]
  });
}
export {
  default_default as default
};
