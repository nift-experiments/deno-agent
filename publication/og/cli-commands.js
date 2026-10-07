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

// authored/_includes/open_graph/cli-commands.jsx
function cli_commands_default({ title, description, openGraphTitle }) {
  if (!openGraphTitle) {
    title = "deno help";
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
      justifyContent: "center",
      background: `radial-gradient(circle 450px at 300px 50%, #273a34, #172723)`,
      fontSize: 28,
      fontWeight: 400,
      padding: "0 90px",
      textWrap: "balance",
      color: "#fff",
      fontFamily: "Inter"
    },
    children: [
      /* @__PURE__ */ jsx("p", {
        style: {
          fontSize: "18px",
          lineHeight: "1",
          marginBottom: "2rem",
          textTransform: "uppercase"
        },
        children: "docs.deno.com"
      }),
      /* @__PURE__ */ jsx("h1", {
        style: {
          margin: "0",
          fontSize: 60,
          fontWeight: 800,
          lineHeight: "1.1",
          marginTop: 0,
          marginLeft: "-16px",
          marginBottom: "2rem"
        },
        children: /* @__PURE__ */ jsx("span", {
          style: {
            background: "#000",
            borderRadius: "10px",
            padding: "10px 18px 4px 18px",
            fontFamily: "Courier",
            lineHeight: "1.2",
            color: "#ffffff",
            textShadow: "0 0 42px #70ffaf, 0 0 36px #70ffaf66, 0 0 28px #70ffaf33, 0 0 16px #70ffaf22, 0 0 8px #70ffaf11"
          },
          children: openGraphTitle
        })
      }),
      /* @__PURE__ */ jsx("p", {
        style: {
          marginTop: 0,
          width: "72%",
          lineHeight: "1.5"
        },
        children: description
      }),
      /* @__PURE__ */ jsx("svg", {
        xmlns: "http://www.w3.org/2000/svg",
        viewBox: "0 0 501 501",
        "stroke-linejoin": "round",
        "stroke-miterlimit": "2",
        "clip-rule": "evenodd",
        style: {
          position: "absolute",
          bottom: "2rem",
          right: "2rem",
          width: "100px",
          height: "100px"
        },
        children: /* @__PURE__ */ jsx("path", {
          fill: "#fff",
          d: "M230 0a220 220 0 1 1-20 440A220 220 0 0 1 230 0Zm52 265-39-5c-8-1-16-3-23-6l-3 1v3c3 4 13 11 21 14-7 6-11 18-13 24a72 72 0 0 0 69 91c23 1 52-10 74-32a200 200 0 1 0-296 0 3 3 0 0 0 5-4c-26-103 31-215 95-250 24-13 47-18 68-10 32 13 50 34 89 52 40 18 44 48 33 78-11 31-46 46-80 44Zm-69-160c-13 1-22 17-23 27-1 11 4 28 21 27 20 0 26-17 24-33-2-13-11-22-22-21Z"
        })
      })
    ]
  });
}
export {
  cli_commands_default as default
};
