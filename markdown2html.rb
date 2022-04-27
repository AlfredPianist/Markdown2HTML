#!/usr/bin/env ruby
require "digest"
require 'active_support'

module MarkdownParser

  SYMBOLS = {
    :h => "#",
    :ul => "-",
    :ol => "*",
  }

  class Parser
    def initialize(src_filename)
      @src_filename = src_filename
      @tag_stack = []
      @output = []
    end

    def parse
      File.open(@src_filename) do |file|
        src_content = file.readlines
        src_content.each do |line|

          if line.blank?
            if @tag_stack.include?(:p)
              @output << "</p>"
              @tag_stack.pop
            end
            next
          end

          symbol = line.split[0]
          symbol_first_char = symbol[0]
          symbol_size = symbol.size
          last_tag = @tag_stack.last

          if !@tag_stack.empty? && SYMBOLS[last_tag] != symbol_first_char && last_tag != :p
            @output << "</#{last_tag}>"
            @tag_stack.pop
          end

          if SYMBOLS.value?(symbol_first_char) || (symbol_first_char == "*" && symbol_size == 1)
            content = format_text(line.split[1..].join(" "))

            case symbol_first_char
            when sym_to_char(:h)
              tag = "h#{symbol_size.clamp(1, 6)}"
              @output << "<#{tag}>#{content}</#{tag}>"
            when sym_to_char(:ul)
              unless @tag_stack.include?(:ul)
                @tag_stack << :ul
                @output << "<ul>"
              end
              @output << "  <li>#{content}</li>"
            when sym_to_char(:ol)
              unless @tag_stack.include?(:ol)
                @tag_stack << :ol
                @output << "<ol>"
              end
              @output << "  <li>#{content}</li>"
            else
              # noop
            end

          else
            if !@tag_stack.include?(:p)
              @tag_stack << :p
              @output << "<p>"
            else
              @output << "    <br />"
            end
            @output << "  #{format_text(line.strip)}"
          end
        end

        unless @tag_stack.empty?
          @output << "</#{@tag_stack[-1].to_s}>"
          @tag_stack.pop
        end
      end

      @output.join "\n"
    end

    private

    def sym_to_char(sym)
      SYMBOLS[sym]
    end

    def format_text(text)
      regexes = {
        b: /\*{2}([^*]*)\*{2}/,
        em: /_{2}([^_]*)_{2}/,
        no_c: /\({2}([^()]*)\){2}/,
        md5: /\[{2}([^\[\]]*)\]{2}/,
      }

      regexes.each do |tag, regex|
        if [:b, :em].include?(tag)
          text.gsub!(regex) do |phrase|
            "<#{tag.to_s}>" << phrase[2..-3] << "</#{tag.to_s}>"
          end
        elsif tag == :md5
          text.gsub!(regex) do |phrase|
            Digest::MD5.hexdigest phrase[2..-3]
          end
        else
          text.gsub!(regex) do |phrase|
            phrase[2..-3].gsub(/[Cc]/, "")
          end
        end
      end

      text
    end
  end
end

begin
  if ARGV.length != 1
    puts "Usage: ./markdown2html.rb README.md README.html"
    exit(false)
  end

  src_filename = ARGV[0]
  puts MarkdownParser::Parser.new(src_filename).parse
  exit(true)
rescue Errno::ENOENT
  puts "Missing #{src_filename}"
  exit(false)
end



