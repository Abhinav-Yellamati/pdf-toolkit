import React from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { Ionicons } from "@expo/vector-icons";

function formatSize(bytes) {
  if (!bytes) return "Unknown size";
  return bytes > 1024 * 1024 ? `${(bytes / 1024 / 1024).toFixed(1)} MB` : `${Math.ceil(bytes / 1024)} KB`;
}

export default function UploadBox({ files, onPick, onClear, multiple }) {
  const totalSize = files.reduce((sum, file) => sum + (file.size || 0), 0);

  return (
    <View style={styles.panel}>
      <Pressable style={styles.target} onPress={onPick}>
        <View style={styles.icon}>
          <Ionicons name="cloud-upload-outline" size={34} color="#ffffff" />
        </View>
        <Text style={styles.title}>Select files</Text>
        <Text style={styles.subtitle}>{multiple ? "Multiple files supported" : "Single file required"} up to 100MB</Text>
      </Pressable>

      {files.length > 0 && (
        <View style={styles.files}>
          <Text style={styles.summary}>
            {files.length} selected - {formatSize(totalSize)}
          </Text>
          {files.map((file) => (
            <View key={`${file.name}-${file.uri}`} style={styles.fileChip}>
              <Text style={styles.fileName} numberOfLines={1}>{file.name}</Text>
              <Text style={styles.fileSize}>{formatSize(file.size)}</Text>
            </View>
          ))}
          <Pressable style={styles.clear} onPress={onClear}>
            <Ionicons name="trash-outline" size={18} color="#e5324f" />
            <Text style={styles.clearText}>Clear</Text>
          </Pressable>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  panel: {
    borderWidth: 1,
    borderStyle: "dashed",
    borderColor: "#8aa4ef",
    borderRadius: 22,
    backgroundColor: "#eef4ff",
    padding: 14,
  },
  target: {
    minHeight: 178,
    alignItems: "center",
    justifyContent: "center",
  },
  icon: {
    width: 68,
    height: 68,
    borderRadius: 22,
    backgroundColor: "#e5324f",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 12,
  },
  title: {
    fontSize: 20,
    color: "#151a2d",
    fontWeight: "900",
  },
  subtitle: {
    color: "#657086",
    marginTop: 6,
  },
  files: {
    marginTop: 12,
  },
  summary: {
    color: "#2454e6",
    fontWeight: "900",
  },
  fileChip: {
    borderWidth: 1,
    borderColor: "#dde5f2",
    borderRadius: 14,
    backgroundColor: "#ffffff",
    padding: 10,
    marginTop: 8,
  },
  fileName: {
    color: "#151a2d",
    fontWeight: "800",
  },
  fileSize: {
    color: "#657086",
    marginTop: 2,
    fontSize: 12,
  },
  clear: {
    flexDirection: "row",
    alignItems: "center",
    alignSelf: "flex-start",
    paddingVertical: 8,
    marginTop: 4,
  },
  clearText: {
    color: "#e5324f",
    fontWeight: "800",
    marginLeft: 6,
  },
});
