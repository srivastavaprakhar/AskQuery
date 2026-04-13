import React from "react";
import { Star } from "lucide-react";
import { cls, timeAgo } from "./utils";

export default function ConversationRow({
  data,
  active,
  onSelect,
  onTogglePin,
  showMeta,
}) {
  const count = Array.isArray(data.messages)
    ? data.messages.length
    : data.messageCount;

  return (
    <div className="group relative">
      {/* Main Row */}
      <div
        onClick={onSelect}
        className={`-mx-1 flex w-[calc(100%+8px)] items-center gap-2 rounded-lg px-2 py-2 cursor-pointer ${
          active ? "bg-zinc-200 dark:bg-zinc-800" : ""
        }`}
      >
        {/* Title */}
        <div className="flex-1 truncate">
          {data.title || "New Chat"}
        </div>

        {/* Pin Button */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            onTogglePin(data.id);
          }}
          title="Pin"
          className="rounded-md p-1 text-zinc-500 opacity-0 transition group-hover:opacity-100 hover:bg-zinc-200 dark:hover:bg-zinc-700"
          aria-label="Pin conversation"
        >
          <Star
            size={16}
            className={data.pinned ? "fill-yellow-400 text-yellow-400" : ""}
          />
        </button>
      </div>

      {/* Tooltip Preview */}
      <div className="pointer-events-none absolute left-[calc(100%+6px)] top-1 hidden w-64 rounded-xl border border-zinc-200 bg-white p-3 text-xs text-zinc-700 shadow-lg dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-200 md:group-hover:block">
        <div className="line-clamp-6 whitespace-pre-wrap">
          {data.preview}
        </div>

        {/* Optional Meta */}
        {showMeta && (
          <div className="mt-2 flex items-center justify-between text-[10px] text-zinc-400">
            <span>{count} msgs</span>
            <span>{timeAgo(data.updatedAt)}</span>
          </div>
        )}
      </div>
    </div>
  );
}