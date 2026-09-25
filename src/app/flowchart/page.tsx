import { Figtree } from "next/font/google";
import Class10Flow from "@/components/class10-flow";

const figtree = Figtree({ subsets: ["latin"], weight: ["400", "500", "600", "700", "800"] });

export const metadata = {
  title: "Class 10 to Career — Perry",
  description: "Tap any step to see every route through it, from Class 10 to the careers it opens.",
};

export default function FlowPage() {
  return <Class10Flow fontFamily={figtree.style.fontFamily} />;
}
