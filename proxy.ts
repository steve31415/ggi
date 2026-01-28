import { NextRequest, NextResponse } from "next/server";

export function proxy(req: NextRequest) {
  const hostname = req.headers.get("host") || "";
  const pathname = req.nextUrl.pathname;

  // Skip rewriting for public/static assets
  const isAsset =
    pathname.startsWith("/_next") ||
    pathname.startsWith("/favicon.ico") ||
    pathname.includes("."); // catches .svg, .png, .js, etc.

  if (isAsset) {
    return NextResponse.next();
  }
  if (hostname.startsWith("thecurve.")) {
    // Rewrite requests to /thecurve folder
    const url = req.nextUrl.clone();
    url.pathname = `/thecurve${url.pathname}`;
    return NextResponse.rewrite(url);
  }

  // Default behavior
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next|favicon.ico).*)"],
};
