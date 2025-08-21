'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Sparkles } from 'lucide-react';
import { ApiService } from '@/services/api';
import { Skeleton } from '@/components/ui/skeleton';

interface GourmetAssistantProps {
  recipeTitle: string;
}

export function GourmetAssistant({ recipeTitle }: GourmetAssistantProps) {
  const [suggestion, setSuggestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [currentQuery, setCurrentQuery] = useState('');

  const handleSuggestion = async (query: string, buttonText: string) => {
    setModalOpen(true);
    setLoading(true);
    setCurrentQuery(buttonText);
    setSuggestion(''); // Clear previous suggestion

    try {
      const result = await ApiService.getAgentSuggestion(recipeTitle, query);
      setSuggestion(result);
    } catch (error) {
      console.error('Agent invocation failed:', error);
      if (error instanceof Error) {
        setSuggestion(`Error: ${error.message}`);
      } else {
        setSuggestion('An unknown error occurred.');
      }
    } finally {
      setLoading(false);
    }
  };

  const suggestionButtons = [
    {
      text: 'Suggest Variations',
      query: 'Suggest 3 creative variations for this recipe.',
    },
    {
      text: 'Suggest Drink Pairings',
      query: 'What drinks would pair well with this?',
    },
    {
      text: 'Give Presentation Tips',
      query: 'How can I best present this dish?',
    },
  ];

  return (
    <Card className="bg-zinc-50 border-zinc-200 mt-8">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-zinc-800">
          <Sparkles className="text-orange-500" />
          Gourmet Assistant
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-zinc-600 mb-4">
          Need some extra inspiration? Ask our AI assistant for tips and ideas.
        </p>
        <div className="flex flex-wrap gap-2">
          {suggestionButtons.map(({ text, query }) => (
            <Button
              key={text}
              variant="outline"
              onClick={() => handleSuggestion(query, text)}
            >
              {text}
            </Button>
          ))}
        </div>
      </CardContent>

      <Dialog open={modalOpen} onOpenChange={setModalOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>{currentQuery}</DialogTitle>
          </DialogHeader>
          <div className="py-4">
            {loading ? (
              <div className="space-y-2">
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-5/6" />
              </div>
            ) : (
              <p className="whitespace-pre-wrap">{suggestion}</p>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </Card>
  );
}
