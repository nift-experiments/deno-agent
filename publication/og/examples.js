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

// authored/_includes/open_graph/examples.jsx
function examples_default({ title, description }) {
  if (!title) {
    title = "Deno documentation";
  }
  if (!description) {
    description = "Learn more at docs.deno.com";
  }
  return /* @__PURE__ */ jsx("div", {
    style: {
      height: "100%",
      width: "100%",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      backgroundColor: "#fff",
      fontSize: 32,
      fontWeight: 600
    },
    children: [
      /* @__PURE__ */ jsx("svg", {
        xmlns: "http://www.w3.org/2000/svg",
        "xml:space": "preserve",
        "fill-rule": "evenodd",
        "stroke-linejoin": "round",
        "stroke-miterlimit": "2",
        "clip-rule": "evenodd",
        version: "1.1",
        viewBox: "0 0 1326 401",
        width: "132px",
        height: "40px",
        position: "absolute",
        children: /* @__PURE__ */ jsx("path", {
          d: "m886 200-1 19H747c6 23 25 37 50 37 21 1 37-8 47-22l35 32c-17 21-46 37-85 37a97 97 0 0 1-102-102c0-60 42-101 98-101 58 0 96 42 96 100Zm-94-54c-22 0-39 12-45 35h87c-5-21-19-35-42-35Zm233-46c42 0 72 23 72 83v117h-53V196c0-37-13-49-38-49-26 0-45 19-45 54v99h-52V103h52v26h1c16-19 39-29 63-29Zm196 203c-62 0-104-43-104-101 0-59 42-102 104-102 61 0 105 41 105 102 0 60-44 101-105 101Zm0-47c29 0 51-23 51-54 0-33-22-55-51-55-31 0-51 24-51 55 0 30 21 54 51 54Zm-721 44V100h73c63 0 104 41 104 100s-38 100-103 100h-74Zm52-48h18c30 0 50-23 50-52 0-30-20-52-46-52h-22v104ZM262 245c34 2 69-13 80-44 11-30 7-60-33-78-39-18-57-39-89-52-21-8-44-3-68 10-64 35-121 147-95 250a3 3 0 0 1-5 3A199 199 0 0 1 215 1a200 200 0 0 1 133 334c-22 22-51 33-74 32a72 72 0 0 1-69-91c2-6 6-18 13-24-8-3-18-10-21-14v-3l3-1c7 3 15 5 23 6l39 5ZM193 85c11-1 20 8 22 21 2 16-4 33-24 33-17 1-22-16-21-27 1-10 10-26 23-27Z"
        })
      }),
      /* @__PURE__ */ jsx("div", {
        style: {
          fontSize: 48,
          fontWeight: 800
        },
        children: title
      }),
      /* @__PURE__ */ jsx("div", {
        children: description
      }),
      /* @__PURE__ */ jsx("p", {
        children: "Examples"
      })
    ]
  });
}
export {
  examples_default as default
};
